import math
import node
import network
import config
import RSSI
import pickle
import simpy


positions =[]



class Interference():
    def __init__(self,time):
        self.time = time
        self.list = []


    def listsetter(self,id):
        self.list.append(id)
        print("l ",self.list )
        print("interfrence happens")


    def listclear(self):
        self.list.clear()
        #print("Clear")


    def network_nodedsicovery(net,distance = config.TX_RANGE):
        print("++++++++++++++++++++ network Table Discovery Begins %d meters ++++++++++++++++++++++++++++"%config.TX_RANGE)
        for n in net.nodes:
            print("Neighbors Table discovery for {0} is below and neighbors are {1}".format(str(n.id),n.neighbors))
            for n1 in net.nodes:
                if(distance > math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2))):
                    if(n!=n1):

                        print("{0} <=> {1} Distance= {2} RSSI= {3}".format(str(n.id) , str(n1.id) , round(math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2)),2),round(RSSI.RSSI_nodes(n,n1)),4))
                        if n1 not in n.neighbors:
                            n.neighbors.append(n1)

        print("+++++++++++++++++++++ network Table Discovery Ends +++++++++++++++++++++++++++++++ \n")


    def distance(self, node ,node1):
        return math.sqrt(((node.x-node1.x)**2)+((node.y-node1.y)**2))

# env = simpy.Environment()

# #interference.network_nodedsicovery(net1)
# in1 = interference(env)
# env.run(100)