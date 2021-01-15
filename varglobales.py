from multiprocessing import Barrier
import multiprocessing

JOURS = 5

#création des barrieres

startDay = multiprocessing.Barrier(2) # on attend que market ait fini ses calculs avant de lancer le jour suivant
startTransac = multiprocessing.Barrier(2)
syncHomes = multiprocessing.Barrier(5) 
endTransac = multiprocessing.Barrier(2)
endDay = multiprocessing.Barrier(1)