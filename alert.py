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
            
            
            
    def run(self):
        while True:
            print("Alert is still exist",self.env.now,self.x,self.y)
            yield self.env.timeout(1)



    def network_nodedsicovery(self,distance = config.TX_RANGE):
        
        print("++++++++++++++++++++ alert Table Discovery Begins %d meters ++++++++++++++++++++++++++++"%config.TX_RANGE)
        for n in self.net.nodes:
                if(distance > math.sqrt(((n.x-self.x)**2)+((n.y-self.y)**2))):
                        print("{0} <=> {1} Distance= {2} RSSI= {3}".format(str(n.id) , "alert" , round(math.sqrt(((n.x-self.x)**2)+((n.y-self.y)**2)),2)))

        print("+++++++++++++++++++++ Alert Table Discovery Ends +++++++++++++++++++++++++++++++ \n")
