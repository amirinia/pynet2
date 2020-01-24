import simpy
import network 
import node
import message
import time
import gui
import config


env = simpy.Environment()



node1 = node.Node(1,env,1.99, 10,10)
node2 = node.Node(2,env,1.98,10,60 ,node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node3 = node.Node(3,env,1.988,30,11)
node4 = node.Node(4,env,1.9088,43,35, node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node5 = node.Node(5,env,1.9855,260,30)
node6 = node.Node(6,env,1.9678,270,50, node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node7 = node.Node(7,env,1.8434,259,72)
node8 = node.Node(8,env,1.90234,241,47)
node9 = node.Node(9,env,1.989364,260,200)
node10 = node.Node(10,env,1.876549,290,200, node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node11 = node.Node(11,env,1.78233 ,280,220 )
node12 = node.Node(12,env,1.79745,20,200 , node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node13 = node.Node(13,env,1.86435,10,160 )
node14 = node.Node(14,env,1.76434 ,13,183 , node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node15 = node.Node(15,env,1.9754734 ,50,200 )
node16 = node.Node(16,env,1.8634754 ,29,189 )
node17 = node.Node(17,env,1.87648 ,35,204 , node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node18 = node.Node(18,env,1.7645,31,172 )
node19 = node.Node(19,env,1.3654675,30,50 )
node20 = node.Node(20,env,1.846 ,130,20 , node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node21 = node.Node(21,env,1.786487,135,2 , node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node22 = node.Node(22,env,2 ,175,5,node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1 )
node23 = node.Node(23,env,1.988,33,14)
node24 = node.Node(24,env,1.9088,57,28, node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node25 = node.Node(25,env,1.9855,252,48)
node26 = node.Node(26,env,1.9678,263,48, node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node27 = node.Node(27,env,1.8434,249,87)
node28 = node.Node(28,env,1.90234,233,35)
node29 = node.Node(29,env,1.989364,253,197)
node30 = node.Node(30,env,1.876549,280,210, node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node31 = node.Node(31,env,1.78233 ,260,210 )
node32 = node.Node(32,env,1.79745,147,130 , node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node33 = node.Node(33,env,1.86435,163,142 )
node34 = node.Node(34,env,1.76434 ,163,145 , node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node35 = node.Node(35,env,1.9754734 ,160,140 )
node36 = node.Node(36,env,1.8634754 ,139,19 )
node37 = node.Node(37,env,1.87648 ,145,20 , node_type=None, power_type=1, mobile_type=0, network=network, sensor_type=1)
node38 = node.Node(38,env,1.7645,141,18 )
node39 = node.Node(39,env,1.3654675,150,17 )

net1 = network.Net(env)

net1.add_node(node1)
net1.add_node(node2)
net1.add_node(node3)
net1.add_node(node4)
net1.add_node(node5)
net1.add_node(node6)
net1.add_node(node7)
net1.add_node(node8)
net1.add_node(node9)
net1.add_node(node10)
net1.add_node(node11)
net1.add_node(node12)
net1.add_node(node13)
net1.add_node(node14)
net1.add_node(node15)
net1.add_node(node16)
net1.add_node(node17)
net1.add_node(node18)
net1.add_node(node19)
net1.add_node(node20)
net1.add_node(node21)
net1.add_node(node22)
net1.add_node(node23)
net1.add_node(node24)
net1.add_node(node25)
net1.add_node(node26)
net1.add_node(node27)
net1.add_node(node28)
net1.add_node(node29)
net1.add_node(node30)
net1.add_node(node31)
net1.add_node(node32)
net1.add_node(node33)
net1.add_node(node34)
net1.add_node(node35)
net1.add_node(node36)
net1.add_node(node37)
net1.add_node(node38)
net1.add_node(node39)


node1.net = net1
node2.net = net1
node3.net = net1
node4.net = net1
node5.net = net1
node6.net = net1
node7.net = net1
node8.net = net1
node9.net = net1
node10.net = net1
node11.net = net1
node12.net = net1
node13.net = net1
node14.net = net1
node15.net = net1
node16.net = net1
node17.net = net1
node18.net = net1
node19.net = net1
node20.net = net1
node21.net = net1
node22.net = net1
node23.net = net1
node24.net = net1
node25.net = net1
node26.net = net1
node27.net = net1
node28.net = net1
node29.net = net1
node30.net = net1
node31.net = net1
node32.net = net1
node33.net = net1
node34.net = net1
node35.net = net1
node36.net = net1
node37.net = net1
node38.net = net1
node39.net = net1

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

