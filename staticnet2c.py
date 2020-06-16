import simpy
import network 
import node
import message
import time
import gui
import config


env = simpy.Environment()




node5 = node.Node(5,env,1.9855,260,30)
node6 = node.Node(6,env,1.9678,270,50)
node7 = node.Node(7,env,1.8434,259,72)
node8 = node.Node(8,env,1.90234,241,47)
# node9 = node.Node(9,env,1.989364,260,200)
# node10 = node.Node(10,env,1.876549,290,200)
# node11 = node.Node(11,env,1.78233 ,280,220 )
node12 = node.Node(12,env,1.79745,20,200 )
node13 = node.Node(13,env,1.86435,10,160 )
node14 = node.Node(14,env,1.76434 ,13,183)
node15 = node.Node(15,env,1.9754734 ,50,200 )
node16 = node.Node(16,env,1.8634754 ,29,189 )
node17 = node.Node(17,env,1.87648 ,35,204)
node18 = node.Node(18,env,1.7645,31,172 )
# node19 = node.Node(19,env,1.3654675,30,50 )
# node20 = node.Node(20,env,1.846 ,130,20 )
# node21 = node.Node(21,env,1.786487,135,2)
# node22 = node.Node(22,env,2 ,175,5)

net1 = network.Net(env)



net1.add_node(node5)
net1.add_node(node6)
net1.add_node(node7)
net1.add_node(node8)

net1.add_node(node12)
net1.add_node(node13)
net1.add_node(node14)
net1.add_node(node15)
net1.add_node(node16)
net1.add_node(node17)
net1.add_node(node18)




node5.net = net1
node6.net = net1
node7.net = net1
node8.net = net1


node12.net = net1
node13.net = net1
node14.net = net1
node15.net = net1
node16.net = net1
node17.net = net1
node18.net = net1



net1.introduce_yourself()
print("KKKKKKKKKK")
net1.network_nodedsicovery()
#graphi = gui.graphic(net1)
#graphi.draw_nods()

# env.run(until=80)

# print(net1.nodes)

# graphi.draw_neighbors()

# net1.network_inboxes()
# net1.network_outboxes()
# net1.network_packet_summery()
# net1.introduce_yourself()

