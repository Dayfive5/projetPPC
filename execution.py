from market import *
from home import *
from varglobales import *
from multiprocessing import Value
import sysv_ipc
import signal
import os
import time

cle_home = 128
cle_market = 129

if __name__ == "__main__":
	try :
		print("------Début de la simulation------")
		#création d'un entier partagé (shared memory)
		condition_meteo = Value('i')
		#Création d'une message queue qui communiquera avec Market
		mq_market = sysv_ipc.MessageQueue(cle_market, sysv_ipc.IPC_CREX)
		#Création d'une message queue qui communiquera avec Home
		mq_home = sysv_ipc.MessageQueue(cle_home, sysv_ipc.IPC_CREX)
		
	   #création et lancement des maisons
		nombre_maison = Value('i',0)
		lock = Lock()
		home_1 = Home(200, 5, 1, cle_home, cle_market, lock, nombre_maison)	
		home_1.start()

		home_2 = Home(5, 155, 1, cle_home, cle_market, lock, nombre_maison)
		home_2.start()


		home_3 = Home(5, 155, 2, cle_home, cle_market, lock, nombre_maison)
		home_3.start()

		home_4 = Home(5, 155, 1, cle_home, cle_market, lock, nombre_maison)
		home_4.start()

		home_5 = Home(200, 5, 2, cle_home, cle_market, lock, nombre_maison)	
		home_5.start()

		print("Dans notre simulation, nous allons nous intéresser à l'échange entre ", nombre_maison.Value, " maisons.")

		#création du Market
		market = Market(condition_meteo, cle_market, lock)

		#création du Weather
		weather = Weather(condition_meteo, lock)

		market.start()
		weather.start()

		#barriere de synchronisation du debut
		debut.wait()

		#envoi du signal du jour 
		i=0
		while (i<JOURS) :
			
			barriere_flag.wait()

			actualisation_tour.wait()
			
			#barrière de fin des transactions entre maisons
			endTransacMaison.wait()

			#barrière 1 de fin des transactions avec market
			endTransacMarket1.wait()

			#envoi d'un signal de fin de transactions
			os.kill(market.pid, signal.SIGSEGV)

			#barrière 2 de fin des transactions avec market
			endTransacMarket2.wait()

			#incrémentation du jour
			i+=1
			startDay.wait()
		

		market.join()
		weather.join()
		home_1.join()
		home_2.join()
		home_3.join()
		home_4.join()
		home_5.join()




	   
	except KeyboardInterrupt :
		print("^C : Keyboard Interruption")


	finally :
		market.terminate()
		weather.terminate()
		mq_home.remove()
		mq_market.remove()
		print("------Fin de la simulation------")