import simpy
import ieee802154 
import node
import message
import time
import gui
import config


env = simpy.Environment()



node1 = node.Node(1,env,1.99, 10,10)
node2 = node.Node(2,env,1.98,10,60 ,node_type=None, power_type=1, mobile_type=0, ieee802154=ieee802154, sensor_type=1)

node5 = node.Node(5,env,1.9855,260,30)
node6 = node.Node(6,env,1.9678,270,50, node_type=None, power_type=1, mobile_type=0, ieee802154=ieee802154, sensor_type=1)

node10 = node.Node(10,env,1.876549,290,200, node_type=None, power_type=1, mobile_type=0, ieee802154=ieee802154, sensor_type=1)
node11 = node.Node(11,env,1.78233 ,280,220 )
node12 = node.Node(12,env,1.79745,20,200 , node_type=None, power_type=1, mobile_type=0, ieee802154=ieee802154, sensor_type=1)
node13 = node.Node(13,env,1.86435,10,160 )


node20 = node.Node(20,env,1.846 ,130,20 , node_type=None, power_type=1, mobile_type=0, ieee802154=ieee802154, sensor_type=1)
node21 = node.Node(21,env,1.786487,135,2 , node_type=None, power_type=1, mobile_type=0, ieee802154=ieee802154, sensor_type=1)

net1 = ieee802154.Net(env)

net1.add_node(node1)
net1.add_node(node2)

net1.add_node(node5)
net1.add_node(node6)

net1.add_node(node10)
net1.add_node(node11)
net1.add_node(node12)
net1.add_node(node13)


net1.add_node(node20)
net1.add_node(node21)


node1.net = net1
node2.net = net1

node6.net = net1


node10.net = net1
node11.net = net1
node12.net = net1
node13.net = net1


node20.net = net1
node21.net = net1



net1.introduce_yourself()
print("KKKKKKKKKK")
net1.ieee802154_nodedsicovery()
#graphi = gui.graphic(net1)
#graphi.draw_nods()

# env.run(until=80)

# print(net1.nodes)

# graphi.draw_neighbors()

# net1.ieee802154_inboxes()
# net1.ieee802154_outboxes()
# net1.ieee802154_packet_summery()
# net1.introduce_yourself()

