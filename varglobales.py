import multiprocessing

JOURS = 5
NB_MAISON = 5

#création des barrieres

debut = multiprocessing.Barrier(NB_MAISON+5) #synchronisation du debut

barriere_flag = multiprocessing.Barrier(NB_MAISON+5) #on attend de reset nos flag avant d'actualiser

actualisation_tour = multiprocessing.Barrier(NB_MAISON+5) #actualise les parametres de chaque objet 

endTransacMaison = multiprocessing.Barrier(NB_MAISON+2) # transactions entre les maisons terminées

endTransacMarket1 = multiprocessing.Barrier(NB_MAISON+1) #premiere etape de la fermeture du market

endTransacMarket2 = multiprocessing.Barrier(NB_MAISON+5) #deuxieme etape de la fermeture du market

startDay = multiprocessing.Barrier(NB_MAISON+5) #on attend que tous les objets aient fini leurs calculs avant de lancer le jour suivant
