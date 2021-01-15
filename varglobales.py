from multiprocessing import Barrier
import multiprocessing

JOURS = 5

#création des barrieres
init = multiprocessing.Barrier(1+5) #execution + 5 maisons
init2 = multiprocessing.Barrier(2) #politics + economics 
startDay = multiprocessing.Barrier(2) # politics + economics
startTransac = multiprocessing.Barrier(2)
syncHomes = multiprocessing.Barrier(5) 
endTransac = multiprocessing.Barrier(2)
endDay = multiprocessing.Barrier(1)