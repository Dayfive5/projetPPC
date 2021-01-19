from multiprocessing import Process, Lock, Value
from threading import Thread, Lock, Semaphore, current_thread
import random
import time
import signal
import sysv_ipc
import concurrent.futures

from politics import *
from economics import *
from varglobales import *



class Market(Process):
	numero_Jour = 0
	#Initialisation
	def __init__(self, conditions_meteo, cle, mutex):
		super().__init__()
		self.prix_energie_init = 0.145
		self.conditions_meteo = conditions_meteo
		self.cle = cle
		self.mutex = mutex
		self.mutex_stock = Lock()
		#Création d'une message queue qui communiquera avec Home
		self.mq_market = sysv_ipc.MessageQueue(self.cle)

		#Présence des facteurs externes
		self.sign_devise = 0 
		self.sign_carburant = 0
		self.sign_tension = 0
		self.sign_guerre = 0

		#stock initial
		self.stockInit = 5000
		self.stock = 0
	   
		#prix init d'1W
		self.prixWattactuel = 0
		self.prixWattavant = 1

		#coef des facteurs externes (politique et economique)
		self.coefGuerre = 1.5
		self.coefTension = 0.75
		self.coefDevise = 0.5
		self.coefPenurie = 0.5

		#coef et présence des facteurs internes (météo et offre/demande)
		self.coefMeteo = 0.5
		self.sign_meteo = 0
		self.sign_baisse = 0
		self.coefBaisse = 0.1
		self.sign_stonks = 0
		self.coefStronks = 0.1

		#fin des transactions avec market
		self.sign_transFin = 0	


		#Gestion des signaux economics et politics
		signal.signal(signal.SIGTERM, self.handler)
		signal.signal(signal.SIGILL, self.handler)
		signal.signal(signal.SIGINT, self.handler)
		signal.signal(signal.SIGUSR2, self.handler)

			
		

	#Gestion des signaux des enfants politics et economics
	def handler(self, sig, frame):

		if sig == signal.SIGTERM:
			#Il y'a une tension diplomatique
			self.sign_tension = 1 
		if sig == signal.SIGILL:
			#Il y'a une guerre
			self.sign_guerre = 1
		if sig == signal.SIGINT:
			#Il y'a une pénurie de carburant
			self.sign_carburant = 1
		if sig == signal.SIGUSR2:
			#Il y'a une crise de devise
			self.sign_devise = 1
		
		if sig == signal.SIGSEGV :
			self.sign_transFin = 1
			

	#Calcul du prix avec les différentes variables
	def calcul_prix_energie(self):
		with self.mutex :
			if (self.conditions_meteo.value < 12) or (self.conditions_meteo.value > 30) :
				self.sign_meteo = 1  
		self.prixWattactuel = 0.8 * self.prixWattavant + self.coefMeteo * self.sign_meteo + self.coefGuerre * self.sign_guerre + self.coefTension * self.sign_tension + self.coefPenurie * self.sign_carburant + self.coefDevise * self.sign_devise - self.coefBaisse * self.sign_baisse + self.coefStronks * self.sign_stonks

		print("Le prix d'un Watt pour ce jour est de ", self.prixWattactuel, "€.") 
		#print("prix av :", self.prixWattavant, "tension", self.sign_tension, "guerre", self.sign_guerre, "devise", self.sign_devise, "penurie", self.sign_carburant, "meteo", self.sign_meteo, self.conditions_meteo.value)
		self.prixWattavant = self.prixWattactuel
		self.sign_baisse = 0
		self.sign_stonks = 0
		

	#Fonction qui remet du stock d'energie dans le market s'il n'y en a plus
	def restock_energie(self):
		self.stock+=self.stockInit


	#Gestion des transactions
	def transactions(self, t, msg):
		#Décodage du message msg	   
		m = msg.decode()
		pid, qte_energie = m.split(";")
		pid = int(pid)
		qte_energie = int(qte_energie)

		#Gestion : Home vend de l'energie
		if t==2 :
			with self.mutex_stock :
				self.stock += qte_energie
				#le prix de l'energie va baisser au jour suivant (car plus d'offre)
				self.sign_baisse += 1

		#Gestion : Home achete de l'energie
		elif t==3 : 
			with self.mutex_stock :
				while qte_energie > self.stock :
					self.restock_energie()
				#le prix de l'energie va monter au jour suivant (car plus de demande)
				self.sign_stonks += 1

		message = "ACK type {0} par ".format(t) + str(pid)
		self.mq_market.send(message.encode(), type=pid)
		print("Fin transaction")


	def resetFlag(self) :
		self.sign_devise = 0 
		self.sign_carburant = 0
		self.sign_tension = 0
		self.sign_guerre = 0
		self.sign_meteo = 0
		


	def run(self):
		try :
			print("Market start")
			politique = Politics()
			economique = Economics()
			politique.start()
			economique.start()

			debut.wait()

			
			i = 0
			while (i<JOURS): 
				
				self.resetFlag()
				barriere_flag.wait()

				actualisation_tour.wait()
				

				if self.sign_tension == 1:
					print("Politique : Il y'a une tension diplomatique")
					
				if self.sign_guerre == 1:
					print("Politique : Il y'a une guerre")

				if self.sign_carburant == 1:
					print("Economie : Il y'a une pénurie de carburant")

				if self.sign_devise == 1:
					print("Economie : Il y'a une crise de devise")
				
				self.calcul_prix_energie()
				endTransacMaison.wait()

				

				#creation d'un pool de threads qui vont gerer les messages queues avec les maisons
				
				with concurrent.futures.ThreadPoolExecutor(max_workers = 3) as executor :
						
					#voir s'il y a messages dans la queue
					while (self.sign_transFin == 0) :
						try:
							msg, t = self.mq_market.receive(block=False)

							if t == 2 or t == 3:
								
								executor.submit(self.transactions, t, msg)
						except sysv_ipc.BusyError:
							time.sleep(0.01)

					self.sign_transFin = 0
					print("fin market jour ")

				endTransacMarket2.wait()					 
						   
				i += 1
				startDay.wait()
				


			politique.join()
			economique.join()

		except:
			politique.terminate()
			economique.terminate()

class Weather(Process):
	def __init__(self, meteo, mutex):
		super().__init__()
		self.meteo = meteo
		self.mutex = mutex
		

	def actualisation(self):
		with self.mutex :
			self.meteo.value = 25 + random.randint(-10,10)
			


	def run (self) :
		print("Weather start")
		debut.wait()

		i=0
		while (i<JOURS):
			barriere_flag.wait()
			self.actualisation()
			print("----------------------------------------")
			print("Jour",i , " : la température est de ", self.meteo.value)
			actualisation_tour.wait()
			endTransacMarket2.wait()
			
			i +=1
			startDay.wait()
			