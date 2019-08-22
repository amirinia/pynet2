import simpy
import network
import math
import config
import time

class Alert():
    def __init__(self, env, x, y, network):
        self.env = env
        self.action = env.process(self.run())
        self.x = x
        self.y = y
        self.net = network
        self.neighbors = []
            
            
    def run(self):
        self.alert_nodedsicovery()
        while self.env.now < config.ALERT_END:
            print("Alert is still exist",self.env.now,self.x,self.y)
            yield self.env.timeout(config.BEACONING_TIME)


    def alert_nodedsicovery(self,distance = config.Alert_RANGE):
        print("\n++++++++++++++++++++ Alert Table Discovery Begins %d meters ++++++++++++++++++++++++++++"%config.Alert_RANGE)
        for n in self.net.nodes:
                if(distance > math.sqrt(((n.x-self.x)**2)+((n.y-self.y)**2))):
                        self.neighbors.append(n)
                        dist = round(math.sqrt(((n.x-self.x)**2)+((n.y-self.y)**2)),2)
                        n.temperature += ( 250 - dist)
                        print("{0} with temp {1} Distance= {2} ".format(str(n.id) , n.temperature , dist))
        print("+++++++++++++++++++++ Alert Table Discovery Ends +++++++++++++++++++++++++++++++ \n")
        time.sleep(5)