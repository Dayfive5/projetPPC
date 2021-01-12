from multiprocessing import Process, Lock, Value
import time
import sysv_ipc
import time 



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
        Home.num += 1
        nombre_maison.Value = Home.num
        mq_home = sysv_ipc.MessageQueue(self.cle_maison, sysv_ipc.IPC_CREAT)
        
    def run(self):
        # politique : 1 = toujours donner 2: toujours vendre 3: vendre s'il n'y a pas de preneur 
        print("La maison ", Home.num , " est dans le marché" )
        time.sleep(5)

        mq_home = sysv_ipc.MessageQueue(self.cle_maison)


    
        if self.politique == 1:
            if 10*self.conso < self.prod:
                don = self.prod-10*self.conso
                self.prod = 10*self.conso
                print("La maison  " ,Home.num, "donne une quantité d'energie  ", don)
                don_byte = str(don).encode()
                mq_home.send(don_byte,type=1)
            elif self.conso > self.prod:
                while (self.conso > self.prod):
                    while(mq_home.current_messages > 0):
                        recup_don,t = mq_home.receive(type=1)
                        valeur_recup = int(recup_don.decode())
                        self.prod = self.prod + valeur_recup
                        print("La maison ",Home.num, "a pu récupérer ", valeur_recup, " d'energie")
                    if (mq_home.current_messages == 0):
                        break
                #si on n'arrive pas à recupérer toute la valeur qu il nous faut des dons on va acheter du market
                if self.prod < self.conso:
                    valeur_achete = self.conso-self.prod
                    print("La maison ",Home.num, "va acheter ", valeur_achete," du market")
                    #Market.vendreAuMaison(valeur_achete)#

                    
        if self.politique == 2:
            if 10*self.conso < self.prod:
                vendre = self.prod-10*self.conso
                self.prod = 10*self.conso
                print("La maison  " ,Home.num, "a vendu au marchet ", vendre )
            while (self.conso > self.prod):
                while(mq_home.current_messages > 0):
                    recup_don,t = mq_home.receive(type=1)
                    valeur_recup = int(recup_don.decode())
                    self.prod = self.prod + valeur_recup
                    #if recup_don.decode() == "":
                    # break
                    print("La maison ",Home.num, "a pu récupérer ", valeur_recup, " d'energie")
                    if (mq_home.current_messages == 0):
                        break
            #si on n'arrive pas à recupérer toute la valeur qu il nous faut des dons on va acheter du market
            if self.prod < self.conso:
                    valeur_achete = self.conso-self.prod
                    print("La maison ",Home.num, "va acheter ", valeur_achete," du market")
                    #Market.vendreAuMaison(valeur_achete)#