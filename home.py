from multiprocessing import Process
import time

class Home(Process):
    def __init__(self, numero_maison, prod_energie ,conso_energie, politique_energie, cle_market, cle_maison) :
        super().__init__()
        self.num = numero_maison
        self.prod = prod_energie
        self.conso = conso_energie
        self.politique = politique_energie
        self.cle_market = cle_market
        self.cle_maison = cle_maison

    def run(self):
        # politique : 1 = toujours donner 2: toujours vendre 3: vendre s'il n'y a pas de preneur 

        #on instancie nos clés
        mh = sysv_ipc.MessageQueue(self.cle_maison)
        mq = sysv_ipc.MessageQueue(self.cle_market)


        #si la consommation d'energie est plus grande que la production, on peut donner/vendre :
        if self.conso < self.prod:

            #if politique is give away : put it in a msg queue
            if self.politique == 1:
                don = str(self.prod-self.conso)
                mh.send(don.encode())

            #if politique is trade with market : sell to market
            elif self.politique == 2:
                vente = str (self.prod-self.conso)
                message = "vendre"
                mq.send(message.encode())
                b = mq.receive()
                if b.decode() == "Combien d'energie"
                    mq.send(vente.encode())

            #if politique is give away and if no takers sell to the market : put it in the home msg queue, if no one take it, sell 
            elif self.politique == 3:
                don_temp = str(self.prod-self.conso)
                timer.start()
                mh.send(don_temp.encode())
                while timer < 20:
                    c = decode(mh.receive())
                    if (c == "merci"):
                        print("la maison", self.num, "a donné de l'énergie")
                        timer.stop()
                        #enelver don_temp de la queue (A CODER)
                if timer > 20
                    #enlever don_temp de la queue (A CODER)
                    timer.stop()
                    message_3 = "vendre"
                    mq.send(message_3.encode())
                    b_3 = mq.receive()
                    if b_3.decode() == "Combien d'energie":
                        mq.send(don_temp.encode())

        elif self.conso > self.prod:
            #if there's a house giving energy in the message queue, take it

            #else buy it at the market
                
    

        #timers : n'existent pas directement en python
        #pour chronometrer du temps il faut:
        #import time
        #t0=time.time()
        #on ecrit notre code
        #t1=time.time()
        #temps_total = t1-t0
        #OU : on ecrit une classe Timer et on l'importe ici

