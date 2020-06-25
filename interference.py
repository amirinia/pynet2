import math
from node import Node
import network
import config
import RSSI
import simpy
import pickle
positions =[]


# positions = pickle.load(open("report/pos.pickle", "rb"))

# env = simpy.Environment()

# net1 = network.Net(env)

# for i in range(len(positions)):
#     print(i)
#     if (i >0):
#         x = positions[i][0]
#         y = net1.ysize - positions[i][1]
#         print("p = x:",positions[i][0],positions[i][1],i)
#         net1.add_node(Node(i,env,2000,x,y,network=net1))

class interference():
    def __init__(self,env):
        self.time = env.now
        self.env = env
        self.list = []
        self.action = env.process(self.run())

    def run(self):
        while True:
            print("hi", env.now)
            yield self.env.timeout(5)


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

env = simpy.Environment()

#interference.network_nodedsicovery(net1)
in1 = interference(env)
env.run(100)