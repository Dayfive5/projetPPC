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
        #entier (shared memory)
        condition_meteo = Value('i')

        #creer message queue home
        #creer home avec en param cle_maison
    
        nombre_maison = Value('i',0)
        lock = Lock()
        home_1 = Home(200, 5, 1,2,lock,nombre_maison)    
        home_1.start()

        home_2 = Home(5,155, 1,2,lock,nombre_maison)
        home_2.start()


        home_3 = Home(5,155, 1,2,lock,nombre_maison)
        home_3.start()

        home_4 = Home(5,155, 1,2,lock,nombre_maison)
        home_4.start()

        home_5 = Home(200, 5, 1,2,lock,nombre_maison)    
        home_5.start()

    
        time.sleep(1)

        
        print("Dans notre simulation, nous allons nous interesser à l'échange entre ",nombre_maison.Value, " maisons")


        #création du Market
        market = Market(condition_meteo, cle_market, lock)

        #création du Weather
        weather = Weather(condition_meteo, lock)

        market.start()
        weather.start()

        #envoi du signal du jour (a coder : toutes les 2 secondes)
        
        i=0
        while (i<5) :
            os.kill(weather.pid, signal.SIGSEGV)
            os.kill(market.pid, signal.SIGUSR1)
            pid_home = [home_1.pid, home_2.pid, home_3.pid, home_4.pid, home_5.pid]
            for p in pid_home :
                os.kill(p, signal.SIGCLD)
            time.sleep(3)
            print("execution", i)
            i+=1
        
        #os.kill(int(home.pid, signal.SIGALRM)
        #time.sleep(3)
        
        #os.kill(int(weather.pid), signal.SIGALRM)
        #os.kill(int(market.pid), signal.SIGALRM)


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
        print("------Fin de la simulation------")