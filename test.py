import sys
import array
from threading import Thread, Lock, Semaphore, current_thread


BUFFER_SIZE = 5
consFlag = True


def weather(n, buffer, full, empty, mutex):
    global consFlag
    i = p = 0
    a, b = 0, 1
    while i < n:
        a, b = b, a+b
        empty.acquire() #Semaphore empty passe de BUFFER_SIZE à BUFFER_SIZE-1, si empty est a 0 (plus de place dans le semaphore), impossible de faire quoi que ce soit, le buffer est plein, il faut attendre que le market consomme
        with mutex: #on bloque le remplissage du buffer pour qu'il ne soit changé que par 1 thread a la fois
            buffer[p] = a
            print(current_thread().name, "produces:", a, "in:", p, flush=True)
            p = (p + 1) % BUFFER_SIZE # p=p+1 modulo BUFFER_SIZE (si il est a 5 il repasse à 0
            i += 1
        full.release()#semaphore release passe de 0 (par ex) à 1 
    consFlag = False

        
def market(buffer, full, empty, mutex):
    i = 0
    while consFlag:
        full.acquire() #semaphore full passe de 1 à 0 (par ex), si full est à 0 (home n'a jamais rien produit), on ne peut pas consommer, il faut att que home release
        with mutex:#on bloque pour que buffer soit change que par 1 thread a la fois
            res = buffer[i]
            print(current_thread().name, "consumes:", res, "from:", i, flush=True)
            i = (i + 1) % BUFFER_SIZE #i=i+1 modulo BUFFER_SIZE
        empty.release()#semaphore release passe de BUFFER_SIZE-1 à BUFFER_SIZE

    
if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("required index argument missing, terminating.")
        sys.exit(1)
        
    try:
        index = int(sys.argv[1])
    except ValueError:
        print("bad index argument: %s, terminating." % sys.argv[1])
        sys.exit(2)
        
    if index < 0:
        print("negative index argument: %d, terminating." % index)
        sys.exit(3)
        

    buffer = array.array('l', range(BUFFER_SIZE)) #on implémente notre memoire partagee (le buffer) de type 'l' (long) et de taille 'BUFFER_SIZE' (=5) 
    
    mutex = Lock()
    full = Semaphore(0) #init 0 place disponible dans le full
    empty = Semaphore(BUFFER_SIZE) #init 5 places disponibles dans le empty
    
    cons = Thread(target=market, args=(buffer, full, empty, mutex))    
    prod = Thread(target=weather, args=(index, buffer, full, empty, mutex))
 
    cons.start()
    prod.start()
    
    cons.join()
    prod.join()
