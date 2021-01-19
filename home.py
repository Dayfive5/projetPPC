from varglobales import *
from multiprocessing import Process, Lock, Value
import time
import sysv_ipc
import time 
import signal
import random
import os




class Home(Process):
	num = 0 
	def __init__(self, prod_energie ,conso_energie, politique_energie,cle_market, mutex, nombre_maison, maisonCom ) :
		super().__init__()
		global cle_home
		self.prod = prod_energie
		self.conso = conso_energie
		self.politique = politique_energie
		self.cle_market = cle_market
		self.mutex = mutex
		self.maisonCom = maisonCom 
		#on définit un stock d'énergie initialement égal à la production
		self.stock = self.prod
		#numérotation des maisons	
		Home.num += 1
		nombre_maison.Value = Home.num
		#messages queue utilisées
		self.mq_market = sysv_ipc.MessageQueue(self.cle_market)


	
	def don_energie(self):
		if self.politique == 1:	
			energieDonnee = self.stock-self.conso
			self.maisonCom.put(energieDonnee)
			print("La maison ", Home.num,"  donne ",energieDonnee, "Watt d'énergie" )
		#if self.politique == 3 :
			#energieDonnee = self.stock-self.conso
			#self.maisonCom.put(energieDonnee)
			#self.stock = self.stock - energieDonnee
			#print("La maison ", Home.num," qui a une politique de donner temporairement (3) donne ",energieDonnee, " d'énergie")
			#time.sleep(0.5)
			#time_end = time.time()+0.05
			# on enlève le message de la queue après un certain temps
			#energie_vendre = 0
			#while (time.time() < time_end )
			#	pass
			#energie_vendre = self.maisonCom.get()
			#self.stock += energie_vendre 

			

			
 
	def demande_energie(self): 
		besoin_energie = self.conso - self.stock
		energie_recue = 0
		while besoin_energie > energie_recue:
			if self.maisonCom.empty():
			#demande au marché
				print("La maison ", Home.num," n'a pas pu récupérer de l'énergie chez les autres maisons")
				break
			else:
				energie_recue += self.maisonCom.get(timeout=0.5)
				print("La maison ", Home.num," a pu récupérer ",energie_recue , "Watt d'énergie chez les autres maisons")
				self.stock += energie_recue

	def run(self):
		print("La maison ", Home.num , " est dans le marché" )
		debut.wait()

		i=0
		while (i<JOURS) :
			#nouveau jour
			barriere_flag.wait()
			
			#actualisation du stock
			self.stock = self.prod 

			#actualisation de la consommation du jour des maisons
			self.conso += random.randint(-50,50)

			if self.conso < 0 :
				self.conso = random.randint(10,200)
			

			actualisation_tour.wait()
			#********Transactions entre les maisons********
			
			#si la consommation est plus grande que la production : home veut récuperer de l'énergie de la maisonCom queue 
			if self.conso > self.stock :
				self.demande_energie()

			#si la consommation est plus petite que la production
			if self.conso < self.stock and (self.politique == 1 or self.politique == 3):
				self.don_energie()
				

			endTransacMaison.wait()
			pid = os.getpid()
			#Si on arrive ici, c'est :
			#soit qu'une maison en manque d'énergie n'en a pas trouvé dans la mq_home 
			#soit qu'une maison veut vendre de l'énergie (politique 2 ou 3 si elle n'a pas trouvé de preneurs)

			#********Transactions avec market********
			
			print("La maison {0} (pid = {1}) debute ses transactions avec market".format(Home.num, pid))
			
			#si la consommation est plus grande que la production alors on achète au marché
			if self.conso > self.stock :
				#on définit notre achat à faire
				achat = self.conso - self.stock 
				#on l'encode avec le pid de la maison
				achat_byte = (str(pid)+";"+str(achat)).encode()
				#on envoie le message à mq_market avec un type 3 (= achat d'énergie)
				self.mq_market.send(achat_byte, type=3)
				#on attend de recevoir une confirmation de message et on print cette validation
				m, _ = self.mq_market.receive(type=pid)
				print(m.decode()+ " qui a recu du marché ", achat, "Watt d'energie")
				#une fois l'énergie reçue, on l'ajoute à notre stock
				self.stock += achat
				

			#si la consommation est plus petite que la production
			elif self.conso < self.stock :
				if self.politique == 2 or self.politique == 3:
					#vendre = l'energie qu'on a en trop
					vendre = self.stock-self.conso
					#on encode la vente en byte et on l'envoie dans la queue du market avec le type 2 (= vente d'énergie)
					vendre_byte = (str(pid)+";"+str(vendre)).encode()
					#on envoie le message à mq_market avec un type 2 (= vente d'énergie)
					self.mq_market.send(vendre_byte, type=2)
					#on attend de recevoir une confirmation de message et on print cette validation
					m, _ = self.mq_market.receive(type=pid)
					print(m.decode() +" qui a vendu au marché ", vendre , "Watt d'energie"  )
					#une fois l'énergie vendue, on l'enlève de notre stock
					self.stock -= vendre
			
			endTransacMarket1.wait()
			
			endTransacMarket2.wait()
			
			#incrémentation du jour
			i+=1
			
			startDay.wait()
					





			


					

			

				
			