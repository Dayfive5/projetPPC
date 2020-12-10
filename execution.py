from market import *
from home import *
from weather import *
from multiprocessing import Array
import sysv_ipc

cle_home = 128
cle_market = 129

if __name__ == "__main__":
    try :
        print("------Début de l'execution du programme------")
        #tableau d'entiers de taille=2 (shared memory)
        condition_meteo = Array('i',2)
    

        #création du Market
        market = Market(condition_meteo, cle_market)
        #création du Weather
        weather = Weather(condition_meteo)

        market.start()
        weather.start()

        market.join()
        weather.join()

    except KeyboardInterrupt :
        print("^C : Keyboard Interruption")

    finally :
        market.terminate()
        weather.terminate()
        print("------Fin de l'execution du programme------")