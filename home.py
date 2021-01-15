from varglobales import *
from multiprocessing import Process, Lock, Value
import time
import sysv_ipc
import time 
import signal



class Home(Process):
	num = 0 
	def __init__(self, prod_energie ,conso_energie, politique_energie, cle_market, mutex, nombre_maison) :
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
		
		#init.wait()

		i=0
		while (i<JOURS) :
			mq_home = sysv_ipc.MessageQueue(self.cle_maison)
			#nouveau jour
			if (self.sign_maison == 1) :
				
				#si la production est plus petite que 10 fois la production
				if 10*self.conso < self.prod :

					#si la maison suit la politique 1 : toujours donner
					if self.politique == 1 :
						#don = l'energie qu'on a en trop
						don = self.prod-10*self.conso
						#reinitialisation de la production ? A CHECKER AVEC NADA
						self.prod = 10*self.conso
						print("La maison ", Home.num, "donne une quantité d'énergie ", don)
						#on encode le don en bytes et on l'envoie dans la queue des maisons avec le type 1 (= don d'énergie)
						don_byte = str(don).encode()
						mq_home.send(don_byte, type=1)

					#si la maison suit la politique 2 : toujours vendre
					if self.politique == 2:
						#vendre = l'energie qu'on a en trop
						vendre = self.prod-10*self.conso
						#A CHECKER AVEC NADA
						self.prod = 10*self.conso
						print("La maison ", Home.num, "veut vendre au marché ", vendre)
						#on encode la vente en byte et on l'envoie dans la queue du market avec le type 2 (= vente d'énergie)
						vendre_byte = str(vendre).encode()
						mq_market.send(vendre_byte, type=2)

					if self.politique == 3 :
						#étape 1 : on met la qté en trop dans la mq des maisons
                        donVente = self.prod-10*self.conso
                        #A CHECKER AVEC NADA
                        self.prod = 10*self.conso
                        print("La maison ", Home.num, "donne une quantité d'énergie ", don)
                        #on encode le don en bytes et on l'envoie dans la queue des maisons avec le type 1 (= don d'énergie)
                        donVente_byte = str(donVente).encode()
                        mq_home.send(donVente_byte, type=1)

                        
                        #barriere qui attend que les transac entre home soient terminées syncHomes
                        #étape 2 : si personne ne la prend on l'enleve de la mq des maisons
                        
                            print("Personne n'a pris le don de la maison ", Home.num, "elle va donc le vendre sur le marché")
                            #on vide la home queue

                            #étape 3 : on met la qté en trop dans la mq du market
                            mq_market.send(donVente_byte, type=2)

                        

				elif self.conso > self.prod:

					while (self.conso > self.prod):
						
						while(mq_home.current_messages > 0):
							try :
								recup_don, t = mq_home.receive(type=1, block=False)
								valeur_recup = int(recup_don.decode())
								self.prod = self.prod + valeur_recup
								#if recup_don.decode() == "":
								# break
								print("La maison ",Home.num, "a pu récupérer ", valeur_recup, " d'energie")

							except sysv_ipc.BusyError :
								time.sleep(0.01)

						if (mq_home.current_messages == 0):
							break
                        #barriere synchHomes

					#si on n'arrive pas à recupérer toute la valeur qu il nous faut des dons on va acheter du market
					if self.conso > self.prod :
						valeur_achete = self.conso-self.prod
						print("La maison ",Home.num, "va acheter ", valeur_achete," du market")
						self.prod = self.prod + valeur_achete
						#Market.vendreAuMaison(valeur_achete)#

				sign_maison = 0
				time.sleep(0.01)
				i+=1