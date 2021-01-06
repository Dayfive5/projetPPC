from multiprocessing import Process
from threading import Lock


class Weather(Process):
    def __init__(self, meteo):
        super().__init__()
        self.meteo = meteo
    

    def run(self):
        mutex = Lock()
        #i=0
        #if signal du jour est appelé (signal = true) :
        with mutex :
    		print("Météo")
    		self.meteo[0]=25
    	
        #a = 25 + random.randint(-5,5)
        #print(a)
        #i+=1
       		#signal = false

        #while True:
        #    pass
