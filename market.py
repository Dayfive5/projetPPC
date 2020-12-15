from multiprocessing import Process
from threading import Thread, Lock, Semaphore, current_thread
import random
import time
import signal

from politics import *
from economics import *
from weather import *


class Market(Process):
    def __init__(self, conditions_meteo, cle):
        super().__init__()
        self.prix_energie_init = 0.145
        self.conditions_meteo = conditions_meteo
        self.cle = cle
        

    #on gere les signaux des enfants
    def handler(self, sig, frame):
        if sig == signal.SIGTERM:
            print("Il y'a une tension diplomatique")
        if sig == signal.SIGILL:
            print("Il y'a une guerre")
        if sig == signal.SIGUSR1:
            print("Il y'a une pénurie de carburant")
        if sig == signal.SIGUSR2:
            print("Il y'a une crise de devise")
    
    def calcul_prix_energie(self):
        #calculer le prix avec les différentes variables
        pass

    def afficher_conditions_meteo(self):
        #afficher les conditions météo
        #lock() ici ? (rwlockwrite ?)
        print([x for x in self.conditions_meteo])

    #fonction transaction(type)
        #lock() pour chaque transaction
        #si type = achat
            #code

         #si type = vente
             #code




    def run(self):
        signal.signal(signal.SIGTERM, self.handler)
        signal.signal(signal.SIGUSR1, self.handler)
        signal.signal(signal.SIGUSR2, self.handler)

        mq_market = sysv_ipc.MessageQueue(self.cle, sysv_ipc.IPC_CREAT)

        while True:
        #creer un pool de threads qui vont gerer les messages queues avec les maisons


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
        
        
        try:
            politique = Politics()
            economique = Economics()
            politique.start()
            economique.start()

            while True:
                time.sleep(2)
                self.afficher_conditions_meteo()

            politique.join()
            economique.join()
        except:
            politique.terminate()
            economique.terminate()

