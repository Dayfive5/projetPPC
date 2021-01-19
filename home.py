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
		self.stock = self.prod
		
				
		Home.num += 1
		nombre_maison.Value = Home.num
		self.mq_home = sysv_ipc.MessageQueue(self.cle_maison)
		self.mq_market = sysv_ipc.MessageQueue(self.cle_market)


		
	def run(self):
		
		print("La maison ", Home.num , " est dans le marché" )
		debut.wait()

		# politique : 1 = toujours donner 2: toujours vendre 3: vendre s'il n'y a pas de preneur 
		

		i=0
		while (i<JOURS) :
			#nouveau jour
			barriere_flag.wait()
				
			#actualisation de la consommation du jour des maisons
			self.conso += random.randint(-50,50)
			if self.conso < 0 :
				self.conso = random.randint(10,200)
			self.stock = self.prod

			actualisation_tour.wait()

			pid = os.getpid()
			#transactions entre homes
			
			#si la consommation est plus grande que la production : home veut recuperer de la mq_home
			if self.conso > self.stock :
				while(self.mq_home.current_messages > 0):
					#print("rentre dans la boucle")
					recup_don, _ = self.mq_home.receive(type=1)


					#Décodage du message msg	   
					m = recup_don.decode()
					pidDon, qte_don = m.split(";")
					pidDon = int(pidDon)
					qte_don = int(qte_don)

					#mise à jour du stock avec le don
					self.stock += qte_don

					#envoi du message de validation de transaction 
					message = "ACK DON PAR : " + str(pidDon)
					self.mq_home.send(message.encode(), type=pidDon)

					print("La maison ", Home.num, "a pu récupérer ", qte_don, " d'energie")
					


			#si la consommation est plus petite que la production
			elif self.conso < self.stock :
				#si la maison suit la politique 1 : toujours donner
				if self.politique == 1 :
					#don = l'energie qu'on a en trop
					don = self.stock-self.conso
					#mise à jour du stock une fois l'energie en trop donnée
					self.stock = self.conso
					#on encode le don en bytes et le pid et on l'envoie dans la queue des maisons avec le type 1 (= don d'énergie)
					don_byte = (str(pid)+";"+str(don)).encode()
					self.mq_home.send(don_byte, type=1)
					
					#On attend la validation de la transaction
					mACK, _ = self.mq_home.receive(type=pid)
					print(mACK.decode())


				if self.politique == 3 :
					pass
			#print("{0} termine ses transactions avec home".format(Home.num))

		

			endTransacMaison.wait()

			

			
			#transactions avec market
			
			#print("{0} debute transactions avec market".format(pid))
			
			#si la consommation est plus grande que la production alors on achete au marché
			if self.conso > self.stock :
				achat = self.conso - self.stock 
				achat_byte = (str(pid)+";"+str(achat)).encode()
				self.mq_market.send(achat_byte, type=3)
				m, _ = self.mq_market.receive(type=pid)

				self.stock += achat
				print(m.decode())

			#si la consommation est plus petite que la production
			elif self.conso < self.stock :
				#si la maison suit la politique 2 : toujours vendre
				#vendre = l'energie qu'on a en trop
				vendre = self.stock-self.conso
				#print("La maison ", Home.num, "veut vendre au marché ", vendre)
				#on encode la vente en byte et on l'envoie dans la queue du market avec le type 2 (= vente d'énergie)
				vendre_byte = (str(pid)+";"+str(vendre)).encode()
				self.mq_market.send(vendre_byte, type=2)
				m, _ = self.mq_market.receive(type=pid)
				print(m.decode())

				self.stock -= vendre
			

			#print("{0} termine ses transactions avec market".format(Home.num))
			endTransacMarket1.wait()
			
			endTransacMarket2.wait()
			

			i+=1
			startDay.wait()





			

			# #si la consommation est plus petite que 10 fois la production
			# if self.conso < self.prod :

			# 	#si la maison suit la politique 1 : toujours donner
			# 	if self.politique == 1 :
			# 		#don = l'energie qu'on a en trop
			# 		don = self.prod-10*self.conso
			# 		#reinitialisation de la production ? A CHECKER AVEC NADA
			# 		self.prod = 10*self.conso
			# 		print("La maison ", Home.num, "donne une quantité d'énergie ", don)
			# 		#on encode le don en bytes et on l'envoie dans la queue des maisons avec le type 1 (= don d'énergie)
			# 		don_byte = str(don).encode()
			# 		self.mq_home.send(don_byte, type=1)

			# 	#si la maison suit la politique 2 : toujours vendre
			# 	if self.politique == 2:
			# 		#vendre = l'energie qu'on a en trop
			# 		vendre = self.prod-10*self.conso
			# 		#A CHECKER AVEC NADA
			# 		self.prod = 10*self.conso
			# 		print("La maison ", Home.num, "veut vendre au marché ", vendre)
			# 		#on encode la vente en byte et on l'envoie dans la queue du market avec le type 2 (= vente d'énergie)
			# 		vendre_byte = str(vendre).encode()
			# 		self.mq_market.send(vendre_byte, type=2)

			# 	if self.politique == 3 :
			# 		#étape 1 : on met la qté en trop dans la mq des maisons
			# 		donVente = self.prod-10*self.conso
			# 		#A CHECKER AVEC NADA
			# 		self.prod = 10*self.conso
			# 		print("La maison ", Home.num, "donne une quantité d'énergie ", don)
			# 		#on encode le don en bytes et on l'envoie dans la queue des maisons avec le type 1 (= don d'énergie)
			# 		donVente_byte = str(donVente).encode()
			# 		self.mq_home.send(donVente_byte, type=1)

					
			# 		#barriere qui attend que les transac entre home soient terminées syncHomes
			# 		#étape 2 : si personne ne la prend on l'enleve de la mq des maisons

			# 		#	print("Personne n'a pris le don de la maison ", Home.num, "elle va donc le vendre sur le marché")
			# 			 #on vide la home queue

			# 			# #étape 3 : on met la qté en trop dans la mq du market
			# 		 #	mq_market.send(donVente_byte, type=2)

					

			# elif self.conso > self.prod:

			# 	while (self.conso > self.prod):
					
			# 		while(self.mq_home.current_messages > 0):
			# 			try :
			# 				recup_don, t = self.mq_home.receive(type=1, block=False)
			# 				valeur_recup = int(recup_don.decode())
			# 				self.prod = self.prod + valeur_recup
			# 				#if recup_don.decode() == "":
			# 				# break
			# 				#enlever le message de la queue

			# 				print("La maison ",Home.num, "a pu récupérer ", valeur_recup, " d'energie")

			# 			except sysv_ipc.BusyError :
			# 				time.sleep(0.01)

			# 		if (self.mq_home.current_messages == 0):
			# 			break
			# 		#barriere synchHomes

			# 	#si on n'arrive pas à recupérer toute la valeur qu il nous faut des dons on va acheter du market
			# 	if self.conso > self.prod :
			# 		valeur_achete = self.conso-self.prod
			# 		print("La maison ",Home.num, "va acheter ", valeur_achete," du market")
			# 		self.prod = self.prod + valeur_achete
			# 		#Market.vendreAuMaison(valeur_achete)#

				
			