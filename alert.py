import simpy
import network
import math
import config

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
        while True:
            print("Alert is still exist",self.env.now,self.x,self.y)
            yield self.env.timeout(1)


    def alert_nodedsicovery(self,distance = config.Alert_RANGE):
        print("++++++++++++++++++++ alert Table Discovery Begins %d meters ++++++++++++++++++++++++++++"%config.TX_RANGE)
        for n in self.net.nodes:
                if(distance > math.sqrt(((n.x-self.x)**2)+((n.y-self.y)**2))):
                        print("{0} <=> {1} Distance= {2} ".format(str(n.id) , "alert" , round(math.sqrt(((n.x-self.x)**2)+((n.y-self.y)**2)),2)))
                        self.neighbors.append(n)
                        n.alert_toggle()
                        n.temperature += 100
                        print(n.temperature,n.alert_neighbor)
        print("+++++++++++++++++++++ Alert Table Discovery Ends +++++++++++++++++++++++++++++++ \n")
