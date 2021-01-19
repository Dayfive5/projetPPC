from multiprocessing import Process
import signal
import random
import os
import time
from varglobales import *


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
		print("Economics start")
		debut.wait()

		carburant = 1/3
		devise = 1/4
		
		i=0
		while (i<JOURS):
			barriere_flag.wait()
			#si nous avons une valeur inférieure à carburant alors il y'a une pénurie de carburant
			if random.random() < carburant:
				self.envoieSignalCarburant()
			#si nous avons une valeur inférieure à devise alors il y'a une crise de devise
			if random.random() < devise:
				self.envoieSignalDevise()

			actualisation_tour.wait()
			endTransacMarket2.wait()
			i+=1
			#incrémentation du jour
			startDay.wait()
