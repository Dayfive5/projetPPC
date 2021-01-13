from multiprocessing import Process, Lock, Value
import signal
import random
import time

class Weather(Process):
	num_jour = 0
	def __init__(self, meteo, mutex):
		super().__init__()
		self.meteo = meteo
		self.mutex = mutex
		self.sign = 0
		signal.signal(signal.SIGSEGV, self.handler)
		

	def handler(self, sig, frame):
		if sig == signal.SIGSEGV :
			Weather.num_jour += 1
			with self.mutex :
				self.meteo.Value = 25 + random.randint(-10,10)
			self.sign = 1


	def run (self) :
		while True :
			if (self.sign==1):
				print("----------------------------------------")
				print("Jour",Weather.num_jour, " : la température est de ", self.meteo.Value)
				self.sign = 0
				time.sleep(0.01)