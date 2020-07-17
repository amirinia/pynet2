import simpy
import ieee802154 
from  node import Node
import message
import time
import gui
import config
import pickle
import io

positions =[]
positions = pickle.load(open("report/pos.pickle", "rb"))

env = simpy.Environment()

net1 = ieee802154.Net(env)
net1.add_node(Node(0, env, 4, (config.xsize)/2, (config.ysize)/2, node_type='B' ,power_type=0,ieee802154 =net1))

for i in range(len(positions)):
    if (i >0):
        x = positions[i][0]
        y = config.ysize - positions[i][1]
        #print("p = x:",positions[i][0],positions[i][1],i)
        net1.add_node(Node(i,env,2000,x,y,ieee802154=net1))
        


net1.introduce_yourself()
if config.printenabled:
    print("static maker KKKKKKKKKK")
net1.ieee802154_nodedsicovery()
graphi = gui.graphic(net1)
#graphi.draw_nods()

# env.run(until=80)

# print(net1.nodes)

# graphi.draw_neighbors()

# net1.ieee802154_inboxes()
# net1.ieee802154_outboxes()
# net1.ieee802154_packet_summery()
# net1.introduce_yourself()

