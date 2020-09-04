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

ieee1 = ieee802154.Net(env)
ieee1.add_node(Node(0, env, 4, (config.xsize)/2, (config.ysize)/2, node_type='B' ,power_type=0,ieee802154 =ieee1))

for i in range(len(positions)):
    if (i >0):
        x = positions[i][0]
        y = config.ysize - positions[i][1]
        #print("p = x:",positions[i][0],positions[i][1],i)
        #print("p = x:",positions[i][0],positions[i][1],i)
        if (i % 2== 0):
                         ieee1.add_node(Node(i,env,2000,x,y,ieee802154=ieee1 ))
        else:
                         ieee1.add_node(Node(i,env,2000,x,y,ieee802154=ieee1, sensor_type=1 ))
        
        


ieee1.introduce_yourself()
if config.printenabled:
    print("static maker KKKKKKKKKK")
ieee1.ieee802154_nodedsicovery()
graphi = gui.graphic(ieee1)
#graphi.draw_nods()

# env.run(until=80)

# print(ieee1.nodes)

# graphi.draw_neighbors()

# ieee1.ieee802154_inboxes()
# ieee1.ieee802154_outboxes()
# ieee1.ieee802154_packet_summery()
# ieee1.introduce_yourself()

