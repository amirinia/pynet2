import math
import node
import network
import config
import RSSI
import simpy
import pickle
import energymodel
import message

class Interference():
    def __init__(self,env,network):
        self.time = env.now
        self.env = env
        self.network = network
        self.list = []
        self.action = env.process(self.run())

    def run(self):
        while True:
            self.list.clear()
            #print("at {0} hi".format(self.env.now))
            self.network_Interfrence()
            #print(self.network.nodes)
            
            yield self.env.timeout(1)


    def network_Interfrence(self):
        distance = config.TX_RANGE
        for n in self.network.nodes:
            for n1 in self.network.nodes:
                if(distance > math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2))):
                    if(n!=n1):
                        if ( n1.flag == True and n.flag == True):
                            self.list.append(n)
                            #print(" Interference {0} <=> {1} Distance= {2} RSSI= {3}".format(str(n.id) , str(n1.id) , round(math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2)),2),round(RSSI.RSSI_nodes(n,n1)),4))
        
        
        if (len(self.list) != len(set(self.list))):
            print(self.list)
            l1= self.list
            print("Interference is detected",set([x for x in l1 if l1.count(x) > 1]))
            for n in l1:
                n.power.decrease_rx_energy(500)


    def distance(self, node ,node1):
        return math.sqrt(((node.x-node1.x)**2)+((node.y-node1.y)**2))

