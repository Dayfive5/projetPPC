from multiprocessing import Process
from threading import Thread, Lock, Semaphore, current_thread
import random
import time
import signal
import sysv_ipc

from politics import *
from economics import *
from weather import *



class Market(Process):
    numero_Jour = 0
    #Initialisation
    def __init__(self, conditions_meteo , cle, mutex):
        super().__init__()
        self.prix_energie_init = 0.145
        self.conditions_meteo = conditions_meteo
        self.cle = cle
        self.sign_jour = 0
        self.sign_devise = 0 
        self.sign_carburant = 0
        self.sign_tension = 0
        self.sign_guerre = 0
        self.stockInit = 5000
        self.mutex = mutex
        #Gestion du jour :
        signal.signal(signal.SIGUSR1, self.handler)
        #Gestion des signaux economics et politics
        signal.signal(signal.SIGTERM, self.handler)
        signal.signal(signal.SIGILL, self.handler)
        signal.signal(signal.SIGINT, self.handler)
        signal.signal(signal.SIGUSR2, self.handler)
        
    #Gestion du nouveau jour
    



    #Gestion des signaux des enfants politics et economics
    def handler(self, sig, frame):
        if sig == signal.SIGUSR1 :
           #Gestion de la meteo
            self.sign_jour +=1
            politique = Politics()
            economique = Economics()
            politique.start()
            economique.start()
            #while True
            politique.join()
            economique.join()
            
        #Calcul du nouveau prix de l'energie
            self.calcul_prix_energie()
        #Gestion des transactions
            self.transactions()
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
        pass

    #Fonction qui remet du stock d'energie dans le market s'il n'y en a plus
    def restock_energie():
        stock+=self.stockInit


    #Gestion des transactions
    def transactions(self):
        pass
        #lock() pour chaque transaction
        #si type = achat
            #code

        #si type = vente
             #codedevise

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

    def vendreAuMaison(quantite_energie):
        stockInit-quantite_energie


    def run(self):
        
        
        #Création d'une message queue qui communiquera avec Home
        mq_market = sysv_ipc.MessageQueue(self.cle, sysv_ipc.IPC_CREAT)

        #creer un pool de threads qui vont gerer les messages queues avec les maisons

        #try:
        #Démarrage des proccessus fils
        #politique = Politics()
        #economique = Economics()
        #politique.start()
        #time.sleep(2)
        #economique.start()

        #while True

        if self.sign_tension == 1:
            print("Politique : Il y'a une tension diplomatique")
        if self.sign_guerre == 1:
            print("Politique : Il y'a une guerre")
        if self.sign_carburant == 1:
            print("Economie : Il y'a une pénurie de carburant")
        if self.sign_devise == 1:
            print("Economie : Il y'a une crise de devise") 
            


        #    politique.join()
        #    economique.join()

        #except:
        #    politique.terminate()
        #    economique.terminate()

       