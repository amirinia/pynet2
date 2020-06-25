
import simpy
import network 
from  node import  Node
import message
import time
import gui
import config
import pickle
import io

positions =[]


positions = pickle.load(open("report/pos.pickle", "rb"))

env = simpy.Environment()

net1 = network.Net(env)

for i in range(len(positions)):
    print(i)
    if (i >0):
        x = positions[i][0]
        y = net1.ysize - positions[i][1]
        print("p = x:",positions[i][0],positions[i][1],i)
        net1.add_node(Node(i,env,2000,x,y,network=net1))
        


net1.introduce_yourself()
print("KKKKKKKKKK")
net1.network_nodedsicovery()
graphi = gui.graphic(net1)
graphi.draw_nods()

# env.run(until=80)

# print(net1.nodes)

# graphi.draw_neighbors()

# net1.network_inboxes()
# net1.network_outboxes()
# net1.network_packet_summery()
# net1.introduce_yourself()

