from multiprocessing import Process

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
        mh = sysv_ipc.MessageQueue(self.cle_maison, sysv_ipc.IPC_CREAT)
        # if self.conso < self.prod:
            # if self.politique == 1:
                # don = str(self.prod-self.conso)
                # mh.send(don.encode())
            # if self.politique == 2:
                # vente = str (self.prod-self.conso)
                # message = "vendre"
                # mq.send(message.encode())
                # b = mq.receive()
                # if b.decode() == "Combien d'energie"
                #    mq.send(vente.encode())
            # if self.politique == 3:
                # don_temp = str(self.prod-self.conso)
                # timer.start()
                # mh.send(don_temp.encode())
                # while timer < 20:
                #   c = decode(mh.receive())
                #   if (c == "merci"):
                #       print("la maison" ,self.num, "a donné de l'énergie")
                #       enelver don_temp de la queue et timer.stop
                # if timer > 20
                #       stop  timer enlever temp de la queue 
                #       message_3 = "vendre"
                #       mq.send(message_3.encode())
                #       b_3 = mq.receive()
                #       if b_3.decode() == "Combien d'energie"
                #           mq.send(don_temp.encode())



        mq = sysv_ipc.MessageQueue(self.cle_market)
        a = mq.receive()
        if a.decode == "Est ce que vous voulez acheter ou vendre ":
            if self.conso > self.prod:
                
            
       
        # actualize the consumption rate depending on the temperature

        #if conso > prod : ask for energy to the other houses
            #if there's a house giving energy in the message queue, take it
            #else buy it at the market

        #if conso < prod : 
            #if politique is trade with market : sell to market
            #if politique is give away : put it in a msg queue
            #if politique is give away and if no takers sell to the market : put it in the msg queue, if no one take it, sell

