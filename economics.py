from multiprocessing import Process
import signal
import random
import os
import time


class Economics(Process):
    def __init__(self):
        super().__init__()

    def envoieSignalCarburant(self):
        #on envoie au processus parent Market le signal SIGTINT s'il y'a une pénurie de carburant
        os.kill(int(os.getppid()), signal.SIGINT)
 
    def envoieSignalDevise(self):
        #on envoie au processus parent Market le signal SIGTUSR2 s'il y'a une crise de devise
        os.kill(int(os.getppid()), signal.SIGUSR2)
    
    def run(self):
        carburant = 10e-8
        devise = 10e-8
        t_end = time.time()+1
        while (time.time() < t_end):
            #si nous avons une valeur inférieure à carburant alors il y'a une pénurie de carburant
            if random.random() < carburant:
                self.envoieSignalCarburant()
            #si nous avons une valeur inférieure à devise alors il y'a une crise de devise
            if random.random() < devise:
                self.envoieSignalDevise()
