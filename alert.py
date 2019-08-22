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
        
        print("++++++++++++++++++++ network Table Discovery Begins %d meters ++++++++++++++++++++++++++++"%config.TX_RANGE)
        for n in self.nodes:
            
            print("Neighbors Table discovery for {0} is below and neighbors are {1}".format(str(n.id),n.neighbors))
            for n1 in self.nodes:
                if(distance > math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2))):
                    if(n!=n1):
                        print("{0} <=> {1} Distance= {2} RSSI= {3}".format(str(n.id) , str(n1.id) , round(math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2)),2),round(RSSI.RSSI_nodes(n,n1)),4))
                        if n1 not in n.neighbors:
                            n.neighbors.append(n1)
                            
        
        print("+++++++++++++++++++++ network Table Discovery Ends +++++++++++++++++++++++++++++++ \n")
