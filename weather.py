from multiprocessing import Process, Lock
import signal
import random

class Weather(Process):
	
	def __init__(self, meteo, mutex):
		super().__init__()
		self.meteo = meteo
		self.mutex = mutex
		self.sign = 0
		

	def handler(self, sig, frame):
		if sig == signal.SIGALRM :
			with self.mutex :
				self.meteo.value = 25 + random.randint(-5,5)
	


	def run (self) :
		signal.signal(signal.SIGALRM, self.handler)
		while True :
			pass