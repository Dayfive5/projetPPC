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

        #Gestion du jour 
        self.sign_jour = 0

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

        #affichage du prix du jour
        self.sign_affPrix = 0

        #lancement du thread pool
        self.sign_transac = 0        

        #Gestion du jour :
        signal.signal(signal.SIGUSR1, self.handler)

        #Gestion des signaux economics et politics
        signal.signal(signal.SIGTERM, self.handler)
        signal.signal(signal.SIGILL, self.handler)
        signal.signal(signal.SIGINT, self.handler)
        signal.signal(signal.SIGUSR2, self.handler)
        

    #Gestion des signaux des enfants politics et economics
    def handler(self, sig, frame):
        if sig == signal.SIGUSR1 :
           #Gestion du jour
            self.sign_jour +=1
            politique = Politics()
            economique = Economics()
            politique.start()
            economique.start()
            
            politique.join()
            economique.join()
            
        #Calcul du nouveau prix de l'energie
            self.sign_affPrix = 1

        #Gestion des transactions entre home et market
            self.sign_transac = 1

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
            

    #Calcul du prix avec les différentes variables
    def calcul_prix_energie(self):
        with self.mutex :
            if (self.conditions_meteo.value < 12) or (self.conditions_meteo.value > 30) :
                self.sign_meteo = 1  
        self.prixWattactuel = 0.8 * self.prixWattavant + self.coefMeteo * self.sign_meteo + self.coefGuerre * self.sign_guerre + self.coefTension * self.sign_tension + self.coefPenurie * self.sign_carburant + self.coefDevise * self.sign_devise - self.coefBaisse * self.sign_baisse + self.coefStronks * self.sign_stonks

        print("Le prix d'un Watt pour ce jour est de ", self.prixWattactuel, "€.") 
        #print("prix av :", self.prixWattavant, "tension", self.sign_tension, "guerre", self.sign_guerre, "devise", self.sign_devise, "penurie", self.sign_carburant, "meteo", self.sign_meteo, self.conditions_meteo.value)
        self.prixWattavant = self.prixWattactuel
        self.sign_meteo = 0
        self.sign_baisse = 0
        self.sign_stonks = 0

    #Fonction qui remet du stock d'energie dans le market s'il n'y en a plus
    def restock_energie(self):
        self.stock+=self.stockInit


    #Gestion des transactions
    def transactions(self, t, msg):
        #Décodage du message msg       
        #pid, qte_energie =

        #Gestion : Home vend de l'energie
        if t==2 :
            with Lock() :
                self.stock += qte_energie
                #le prix de l'energie va baisser au jour suivant (car plus d'offre)
                self.sign_baisse += 1

        #Gestion : Home achete de l'energie
        if t==3 : 
            with Lock() :
                if qte_energie > self.stock :
                    restock_energie()
                #le prix de l'energie va monter au jour suivant (car plus de demande)
                self.sign_stonks += 1

       

        #if stock < demande d'achat -> restock_energie()

        #ce qu'il faut faire devisepour communiquer
            #revoir td4 car besoin d'envoyer le pid de la maison pour lui rep

            #a = mq_market.receive()
            #if a.decode() == "achete":
                #message_1 = "Combien d'energie"
                #mq_market.send(message_1.encode())
                #appel fonction transaction(achat)

            #if a.decode() == "vendre":
                #message_2 = "Combien d'energie"
                #mq_market.send(message_2.encode())
                #value_v = mq_market.receive()
                #value = int(value_v.decode())
                #appel fonction transaction(vente)


    def run(self):
        #Création d'une message queue qui communiquera avec Home
        mq_market = sysv_ipc.MessageQueue(self.cle, sysv_ipc.IPC_CREAT)

        i = 0
        while True :
            if(i<JOURS):
                print("market", i)
                
                if self.sign_affPrix == 1 :
                    self.calcul_prix_energie()
                    self.sign_affPrix = 0
                    time.sleep(0.01)

                if self.sign_tension == 1:
                    print("Politique : Il y'a une tension diplomatique")
                    self.sign_tension = 0
                    time.sleep(0.01)

                if self.sign_guerre == 1:
                    print("Politique : Il y'a une guerre")
                    self.sign_guerre = 0
                    time.sleep(0.01)

                if self.sign_carburant == 1:
                    print("Economie : Il y'a une pénurie de carburant")
                    self.sign_carburant = 0
                    time.sleep(0.01)

                if self.sign_devise == 1:
                    print("Economie : Il y'a une crise de devise")
                    self.sign_devise = 0 
                    time.sleep(0.01)

                #barriere

                #creer un pool de threads qui vont gerer les messages queues avec les maisons
                if self.sign_transac == 1 :
                    self.sign_transac = 0
                    with concurrent.futures.ThreadPoolExecutor(max_workers = 3) as executor :
                        print("Début des transactions avec market")
                            
                        #voir s'il y a messages dans la queue
                        print("Checking des messages recus dans la queue Market")
                        while True :
                            try :
                                msg, t = mq_market.receive(block=False)
                                break
                                #print("mesg", mq_market.current_messages)
                            except sysv_ipc.BusyError:
                                time.sleep(0.01)
                                
                            #si oui, identifier son type : si son type est valide on envoie le message à la fonction transactions
                            if t == 1 or t == 2 :
                                print("Message recu valide")
                                executor.submit(self.transactions, t, msg)

                            elif (mq_market.current_messages == 0):
                                print("Fin des transactions")
                                
                #barriere
                           

                i += 1
                time.sleep(3)

            else :
                break
            


        #    politique.join()
        #    economique.join()

        #except:
        #    politique.terminate()
        #    economique.terminate()

class Weather(Process):
	num_jour = 0
	def __init__(self, meteo, mutex):
		super().__init__()
		self.meteo = meteo
		self.mutex = mutex
		self.sign = 0
		signal.signal(signal.SIGSEGV, self.handler)
		

	def handler(self, sig, frame):
		if sig == signal.SIGSEGV :
			Weather.num_jour += 1
			with self.mutex :
				self.meteo.value = 25 + random.randint(-10,10)
			self.sign = 1


	def run (self) :
		i=0
		while True:
			if(i<JOURS):
				if (self.sign==1):
					print("----------------------------------------")
					print("Jour",Weather.num_jour, " : la température est de ", self.meteo.value)
					self.sign = 0
					time.sleep(0.01)
					i +=1
			else : 
				break  