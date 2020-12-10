from multiprocessing import Process
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
        pass

    def afficher_conditions_meteo(self):
        print([x for x in self.conditions_meteo])


    def run(self):
        signal.signal(signal.SIGTERM, self.handler)
        signal.signal(signal.SIGUSR1, self.handler)
        signal.signal(signal.SIGUSR2, self.handler)

        mq_market = sysv_ipc.MessageQueue(self.cle, sysv_ipc.IPC_CREAT)

        while True:
            message_acceuil = "Est ce que vous voulez acheter ou vendre "
            mq_market.send(message_acceuil.encode())
            a = mq_market.receive()
            if a.decode() == "achete":
                message_1 = "Combien d'energie"
                mq_market.send(message_1.encode())

            if a.decode() == "vendre":
                message_2 = "Combien d'energie"
                mq_market.send(message_2.encode())
                value_v = mq_market.receive()
                value = int(value_v.decode())
        
        
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

