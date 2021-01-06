from multiprocessing import Process
from threading import Lock

class Weather(Process):
    def __init__(self, meteo):
        super().__init__()
        self.meteo = meteo
    

    def run(self):
        i=0
        #if signal du jour est appelé (signal = true) :
        	with Lock() :
    			print("Météo")
        		self.meteo[i]= 25 + random.randint(-5,5)
        		i+=1
       		#signal = false

        while True:
            pass
