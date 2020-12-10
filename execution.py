from market import *
from home import *
from weather import *
from multiprocessing import Array
import sysv_ipc

cle_home = 128
cle_market = 129

if __name__ == "__main__":
    print("Excution du programme")
    #tableau d'entiers (shared memory)
    condition_meteo = Array('i',2)
    

    market = Market(condition_meteo, cle_market)
    weather = Weather(condition_meteo)

    market.start()
    weather.start()

    market.join()
    weather.join()

    print("Fin execution")