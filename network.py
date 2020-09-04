import simpy
import ieee802154 
from node import Node
import message
import time
import gui
import config


        # self.xsize = xsize
        # self.ysize = ysize

env = simpy.Environment()

ieee1 = ieee802154.Net(env)


ieee1.add_node(Node(0, env, 4, (config.xsize)/2, (config.ysize)/2, node_type='B' ,power_type=0,ieee802154 =ieee1))
ieee1.add_node(Node(1,env,1.99, 10,10,ieee802154 =ieee1))
ieee1.add_node(Node(2,env,1.98,10,60,ieee802154 =ieee1, sensor_type=1))
ieee1.add_node(Node(3,env,1.988,30,11,ieee802154 =ieee1))
ieee1.add_node(Node(4,env,1.9088,43,35,ieee802154 =ieee1, sensor_type=1))
ieee1.add_node(Node(5,env,1.9855,260,30,ieee802154 =ieee1))
ieee1.add_node(Node(6,env,1.9678,270,50,ieee802154 =ieee1, sensor_type=1))
ieee1.add_node(Node(7,env,1.8434,259,72,ieee802154 =ieee1))
ieee1.add_node(Node(8,env,1.90234,241,47,ieee802154 =ieee1, sensor_type=1))
ieee1.add_node(Node(9,env,1.989364,260,200,ieee802154 =ieee1))
ieee1.add_node(Node(10,env,1.876549,290,200,ieee802154 =ieee1, sensor_type=1))
ieee1.add_node(Node(11,env,1.78233 ,280,220 ,ieee802154 =ieee1))
ieee1.add_node(Node(12,env,1.79745,20,200,ieee802154 =ieee1 , sensor_type=1))
ieee1.add_node(Node(13,env,1.86435,10,160,ieee802154 =ieee1 ))
ieee1.add_node(Node(14,env,1.76434 ,13,183,ieee802154 =ieee1, sensor_type=1))
ieee1.add_node(Node(15,env,1.9754734 ,50,200,ieee802154 =ieee1 ))
ieee1.add_node(Node(16,env,1.8634754 ,29,189,ieee802154 =ieee1, sensor_type=1 ))
ieee1.add_node(Node(17,env,1.87648 ,35,204,ieee802154 =ieee1))
ieee1.add_node(Node(18,env,1.7645,31,172,ieee802154 =ieee1, sensor_type=1 ))
ieee1.add_node(Node(19,env,1.3654675,30,50,ieee802154 =ieee1 ))
ieee1.add_node(Node(20,env,1.846 ,130,20,ieee802154 =ieee1 , sensor_type=1))
ieee1.add_node(Node(21,env,1.786487,135,2,ieee802154 =ieee1))
ieee1.add_node(Node(22,env,2 ,175,5,ieee802154 =ieee1, sensor_type=1))



ieee1.introduce_yourself()
print("satatic net KKKKKKKKKK")
ieee1.ieee802154_nodedsicovery()
graphi = gui.graphic(ieee1)
graphi.draw_nods()

# env.run(until=80)

# print(ieee1.nodes)

# graphi.draw_neighbors()

# ieee1.ieee802154_inboxes()
# ieee1.ieee802154_outboxes()
# ieee1.ieee802154_packet_summery()
# ieee1.introduce_yourself()

