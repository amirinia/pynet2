import random

Sensor_Type = {0: "Alert-Temperature", 1: "Monitoring"}
class sensor:
    def __init__(self,id,name,Sensor_Type=1):
        self.id = id
        self.name = name
        self.sensor_type = Sensor_Type

    def __str__(self):
        return str(self.sensor_type)

    def __repr__(self):
        return str("sensor"+str(self.sensor_type))

    def run(self,env):
        if self.sensor_type == 0:
            print(self.temperature_sensor())
        print(self.light_sensor())
        print(self.temperature_sensor())

    def temperature_sensor(self):
        return random.randint(17,30)
        
    def light_sensor(self):
        return random.randint(100,300)

    def humidity_sensor(self):
        return random.randint(171 , 194)

    #pressure

    
