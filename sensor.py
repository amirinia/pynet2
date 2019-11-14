import random

Sensor_Type = {0: "Temp", 1: "Monitoring"}
class sensor:
    def __init__(self,id,name,Sensor_Type=1):
        self.id = id
        self.name = name
        self.sensor_type = Sensor_Type

    def run(self,env):
        if self.sensor_type == 0:
            print(self.temperature_sensor())
        print(self.light_sensor())

    def temperature_sensor(self):
        return random.randint(17,30)
        

    def light_sensor(self):
        return random.randint(100,300)

        

    
