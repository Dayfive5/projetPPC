from varglobales import *
from multiprocessing import Process, Lock, Value
import time
import sysv_ipc
import time 
import signal
import random
import os



class Home(Process):
	num = 0 
	def __init__(self, prod_energie ,conso_energie, politique_energie, cle_maison, cle_market, mutex, nombre_maison) :
		super().__init__()
		global cle_home
		self.prod = prod_energie
		self.conso = conso_energie
		self.politique = politique_energie
		self.cle_market = cle_market
		self.cle_maison = cle_maison
		self.mutex = mutex
		#on définit un stock d'énergie initialement égal à la production
		self.stock = self.prod
		#numérotation des maisons	
		Home.num += 1
		nombre_maison.Value = Home.num
		#messages queue utilisées
		self.mq_home = sysv_ipc.MessageQueue(self.cle_maison)
		self.mq_market = sysv_ipc.MessageQueue(self.cle_market)


		
	def run(self):
		print("La maison ", Home.num , " est dans le marché" )
		debut.wait()

		i=0
		while (i<JOURS) :
			#nouveau jour
			barriere_flag.wait()
			
			#actualisation du stock
			self.stock = self.prod 

			#actualisation de la consommation du jour des maisons
			self.conso += random.randint(-50,50)
			if self.conso < 0 :
				self.conso = random.randint(10,200)
			

			actualisation_tour.wait()

			
			
			#********Transactions entre les maisons********

			#si la consommation est plus grande que la production : home veut récuperer de l'énergie de la mq_home
			#if self.conso > self.stock :
				# while(self.mq_home.current_messages > 0):
				# 	#print("rentre dans la boucle")
				# 	recup_don, _ = self.mq_home.receive(type=1)
				# 	#Décodage du message msg	   
				# 	m = recup_don.decode()
				# 	pidDon, qte_don = m.split(";")
				# 	pidDon = int(pidDon)
				# 	qte_don = int(qte_don)
				# 	#mise à jour du stock avec le don
				# 	self.stock += qte_don
				# 	#envoi du message de validation de transaction 
				# 	message = "ACK DON PAR : " + str(pidDon)
				# 	self.mq_home.send(message.encode(), type=pidDon)
				# 	print("La maison ", Home.num, "a pu récupérer ", qte_don, " d'energie")
				# 	if (self.mq_home.current_messages == 0):
				# 		break
				
			#si la consommation est plus petite que la production
			#elif self.conso < self.stock :
				#si la maison suit la politique 1 : toujours donner
				#if self.politique == 1 :
				# 	#don = l'energie qu'on a en trop
				# 	don = self.stock-self.conso
				# 	#mise à jour du stock une fois l'energie en trop donnée
				# 	self.stock = self.conso
				# 	#on encode le don en bytes et le pid et on l'envoie dans la queue des maisons avec le type 1 (= don d'énergie)
				# 	don_byte = (str(pid)+";"+str(don)).encode()
				# 	self.mq_home.send(don_byte, type=1)
				# 	#On attend la validation de la transaction
				# 	mACK, _ = self.mq_home.receive(type=pid)
				# 	print(mACK.decode())

				#elif self.politique == 3 :
					# #donVente = l'energie qu'on a en trop
					# donVente = self.stock-self.conso
					# #mise à jour du stock une fois l'énergie en trop donnée
					# self.stock = self.conso
					# #on encode le don en bytes et le pid et on l'envoie dans la queue des maisons avec le type 1 (= don d'énergie)
					# donVente_byte = (str(pid)+";"+str(donVente)).encode()
					# self.mq_home.send(donVente_byte, type=1)
					# #si pas de preneurs, on enleve le message de la queue
					# #on remet à jour notre stock
					# self.stock = self.prod + self.conso
					# #et on enverra le message à la mq de market à la place
		
			endTransacMaison.wait()
			pid = os.getpid()
			#Si on arrive ici, c'est :
			#soit qu'une maison en manque d'énergie n'en a pas trouvé dans la mq_home 
			#soit qu'une maison veut vendre de l'énergie (politique 2 ou 3 si elle n'a pas trouvé de preneurs)

			#********Transactions avec market********
			
			print("La maison {0} (pid = {1}) debute ses transactions avec market".format(Home.num, pid))
			
			#si la consommation est plus grande que la production alors on achète au marché
			if self.conso > self.stock :
				#on définit notre achat à faire
				achat = self.conso - self.stock 
				#on l'encode avec le pid de la maison
				achat_byte = (str(pid)+";"+str(achat)).encode()
				#on envoie le message à mq_market avec un type 3 (= achat d'énergie)
				self.mq_market.send(achat_byte, type=3)
				#on attend de recevoir une confirmation de message et on print cette validation
				m, _ = self.mq_market.receive(type=pid)
				print(m.decode())
				#une fois l'énergie reçue, on l'ajoute à notre stock
				self.stock += achat
				

			#si la consommation est plus petite que la production
			elif self.conso < self.stock :
				#vendre = l'energie qu'on a en trop
				vendre = self.stock-self.conso
				#on encode la vente en byte et on l'envoie dans la queue du market avec le type 2 (= vente d'énergie)
				vendre_byte = (str(pid)+";"+str(vendre)).encode()
				#on envoie le message à mq_market avec un type 2 (= vente d'énergie)
				self.mq_market.send(vendre_byte, type=2)
				#on attend de recevoir une confirmation de message et on print cette validation
				m, _ = self.mq_market.receive(type=pid)
				print(m.decode())
				#une fois l'énergie vendue, on l'enlève de notre stock
				self.stock -= vendre
			
			endTransacMarket1.wait()
			
			endTransacMarket2.wait()
			
			#incrémentation du jour
			i+=1
			
			startDay.wait()





			


					

			

				
			