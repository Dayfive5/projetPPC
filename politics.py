from multiprocessing import Process
import signal
import random
import os
import time

class Politics(Process):
    def __init__(self):
        super().__init__()

    def envoieSignalTension(self):
        #on envoie au processus parent Market le signal SIGTERM s'il y'a une tension diplomatique 
        os.kill(int(os.getppid()), signal.SIGTERM)

    def envoieSignalGuerre(self):
        #on envoie au processus parent Market le signal SIGTERM s'il y'a une tension diplomatique 
        os.kill(int(os.getppid()), signal.SIGILL)

    def run(self):
        tension = 10e-8
        guerre = 10e-9
        t_end = time.time()+1
        while (time.time()<t_end):
            #si nous avons une valeur inférieur à tension alors il y'a une tension diplomatique
            if random.random() < tension :
                self.envoieSignalTension()
            if random.random() < tension :
                self.envoieSignalGuerre()
               
            


