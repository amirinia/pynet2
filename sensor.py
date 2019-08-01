import random


class sensor:
    def __init__(self,id,name):
        self.id = id
        self.name = name

    def run(self,env):
        print(self.temperature_sensor())
        print(self.light_sensor())

    def temperature_sensor(self):
        return random.randint(17,30)
        

    def light_sensor(self):
        return random.randint(100,300)

        

    
