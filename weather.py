from multiprocessing import Process

class Weather(Process):
    def __init__(self, meteo):
        super().__init__()
        self.meteo = meteo
    

    def run(self):
        print("Méteo")
        self.meteo[0]= 25
        while True:
            pass
