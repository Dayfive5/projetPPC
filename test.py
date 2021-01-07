from multiprocessing import Process, Lock
import signal
import random

class Weather(Process):
	#mutex = Lock()
	def __init__(self, meteo):
		super().__init__()
		self.meteo = meteo

	def handler(self, sig, frame):
		if sig == signal.ALRM :
			with mutex :
				print("Météo")
				self.meteo= 25 + random.randint(-5,5)
				

	def run (self) :
		
		with Lock() :
			print("Météo")
			self.meteo= 25 + random.randint(-5,5)
			print(self.meteo)

if __name__=="__main__":
	meteo = 0
	p=Weather(meteo)
	p.start()
	p.join()
