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

    #Initialisation
    def __init__(self, conditions_meteo, cle, mutex):
        super().__init__()
        self.prix_energie_init = 0.145
        self.conditions_meteo = conditions_meteo
        self.cle = cle
        self.sign = 0
        self.stockInit = 500
        self.mutex = mutex
        #Gestion du jour :
        signal.signal(signal.SIGALRM, self.handlerJour)
        #Gestion des signaux economics et politics
        signal.signal(signal.SIGTERM, self.handler)
        signal.signal(signal.SIGILL, self.handler)
        signal.signal(signal.SIGUSR1, self.handler)
        signal.signal(signal.SIGUSR2, self.handler)
        
    #Gestion du nouveau jour
    def handlerJour(self, sig, frame):

        #Gestion de la meteo
        self.sign = 5

        #Calcul du nouveau prix de l'energie
        self.calcul_prix_energie()

        #Gestion des transactions
        self.transactions()



    #Gestion des signaux des enfants politics et economics
    def handler(self, sig, frame):
        if sig == signal.SIGTERM:
            #Il y'a une tension diplomatique
            self.sign = 1 
        if sig == signal.SIGILL:
            #Il y'a une guerre
            self.sign = 2
        if sig == signal.SIGUSR1:
            #Il y'a une pénurie de carburant
            self.sign = 3
        if sig == signal.SIGUSR2:
            #Il y'a une crise de devise
            self.sign = 4
            

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
             #code

        #if stock < demande d'achat -> restock_energie()

        #ce qu'il faut faire pour communiquer
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

        #creer un pool de threads qui vont gerer les messages queues avec les maisons

        try:
            #Démarrage des proccessus fils
            politique = Politics()
            economique = Economics()
            politique.start()
            economique.start()

            while True:

                if self.sign == 1:
                    print("Politique : Il y'a une tension diplomatique")
                    self.sign = 0
                elif self.sign == 2:
                    print("Politique : Il y'a une guerre")
                    self.sign = 0
                elif self.sign == 3:
                    print("Economie : Il y'a une pénurie de carburant")
                    self.sign = 0
                elif self.sign == 4:
                    print("Economie : Il y'a une crise de devise") 
                    self.sign = 0
                elif self.sign == 5:
                    print("Météo : ", self.conditions_meteo.value)
                    self.sign = 0
                #self.sign = 0

            politique.join()
            economique.join()

        except:
            politique.terminate()
            economique.terminate()

       