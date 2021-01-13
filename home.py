from multiprocessing import Process, Lock, Value
import time
import sysv_ipc
import time 
import signal



class Home(Process):
    num = 0 
    def __init__(self, prod_energie ,conso_energie, politique_energie, cle_market, mutex,nombre_maison) :
        super().__init__()
        global cle_home
        self.prod = prod_energie
        self.conso = conso_energie
        self.politique = politique_energie
        self.cle_market = cle_market
        self.cle_maison = 128
        self.mutex = mutex
        self.sign_maison = 0
        Home.num += 1
        nombre_maison.Value = Home.num
        mq_home = sysv_ipc.MessageQueue(self.cle_maison, sysv_ipc.IPC_CREAT)
        signal.signal(signal.SIGCLD, self.handler)

    def handler (self, sig, frame) :
        if (sig == signal.SIGCLD):
            self.sign_maison = 1
        
    def run(self):
        # politique : 1 = toujours donner 2: toujours vendre 3: vendre s'il n'y a pas de preneur 
        print("La maison ", Home.num , " est dans le marché" )
        time.sleep(5)

        i=0
        while (i<5) :
            mq_home = sysv_ipc.MessageQueue(self.cle_maison)
            if (self.sign_maison == 1) :
                
                if 10*self.conso < self.prod :

                    if self.politique == 1 :
                        don = self.prod-10*self.conso
                        self.prod = 10*self.conso
                        print("La maison ", Home.num, "donne une quantité d'energie ", don)
                        don_byte = str(don).encode()
                        mq_home.send(don_byte,type=1)

                    if self.politique == 2:
                        vendre = self.prod-10*self.conso
                        self.prod = 10*self.conso
                        print("La maison ", Home.num, "a vendu au marchet ", vendre )

                    if self.politique == 3 :
                        pass

                elif self.conso > self.prod:

                    while (self.conso > self.prod):
                        while(mq_home.current_messages > 0):
                            recup_don, t = mq_home.receive(type=1)
                            valeur_recup = int(recup_don.decode())
                            self.prod = self.prod + valeur_recup
                            #if recup_don.decode() == "":
                            # break
                            print("La maison ",Home.num, "a pu récupérer ", valeur_recup, " d'energie")
                        if (mq_home.current_messages == 0):
                            break
                    #si on n'arrive pas à recupérer toute la valeur qu il nous faut des dons on va acheter du market
                    if self.conso > self.prod :
                        valeur_achete = self.conso-self.prod
                        print("La maison ",Home.num, "va acheter ", valeur_achete," du market")
                        self.prod = self.prod + valeur_achete
                        #Market.vendreAuMaison(valeur_achete)#

                sign_maison = 0
                time.sleep(0.01)
                i+=1