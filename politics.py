from multiprocessing import Process
import signal
import random
import os
import time
from varglobales import *

class Politics(Process):
	def __init__(self):
		super().__init__()

	def envoieSignalTension(self):
		#on envoie au processus parent Market le signal SIGTERM s'il y'a une tension diplomatique 
		os.kill(int(os.getppid()), signal.SIGTERM)

	def envoieSignalGuerre(self):
		#on envoie au processus parent Market le signal SIGILL s'il y'a une guerre 
		os.kill(int(os.getppid()), signal.SIGILL)

	def run(self):
		print("Politics start")
		debut.wait()
		tension = 1/2
		guerre = 1/5
		i=0
		while (i<JOURS):
			barriere_flag.wait()
			#si nous avons une valeur inférieure à tension alors il y'a une tension diplomatique
			if random.random() < tension :
				self.envoieSignalTension()
			#si nous avons une valeur inférieure à guerre alors il y'a une guerre
			if random.random() < guerre :
				self.envoieSignalGuerre()
			actualisation_tour.wait()
			endTransacMarket2.wait()
			#incrémentation du jour
			i+=1
			startDay.wait()

			