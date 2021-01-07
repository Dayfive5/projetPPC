from market import *
#from home import *
from weather import *
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
        #entier (shared memory)
        condition_meteo = Value('i')

        #creer message queue home
        #creer home avec en param cle_maison
    
        mutex = Lock()

        #création du Market
        market = Market(condition_meteo, cle_market, mutex)

        #création du Weather
        weather = Weather(condition_meteo, mutex)

        market.start()
        weather.start()

        #envoi du signal du jour (envoie un SIGALRM) (a coder : toutes les 10 secondes)
        os.kill(int(weather.pid), signal.SIGALRM)
        os.kill(int(market.pid), signal.SIGALRM)
        #os.kill(int(home.pid, signal.SIGALRM)
        time.sleep(3)
        
        os.kill(int(weather.pid), signal.SIGALRM)
        os.kill(int(market.pid), signal.SIGALRM)


        market.join()
        weather.join()


       
    except KeyboardInterrupt :
        print("^C : Keyboard Interruption")

    finally :
        market.terminate()
        weather.terminate()
        print("------Fin de la simulation------")