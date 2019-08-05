import simpy
import network 
import node
import message
import time
import gui
import config


env = simpy.Environment()



node1 = node.Node(1,env,2, 10,10)
node2 = node.Node(2,env,2,10,60)
node3 = node.Node(3,env,2,30,11)
node4 = node.Node(4,env,2,43,35)
node5 = node.Node(5,env,2,260,30)
node6 = node.Node(6,env,2,270,50)
node7 = node.Node(7,env,2,259,72)
node8 = node.Node(8,env,2,241,47)
node9 = node.Node(9,env,2,260,200)
node10 = node.Node(10,env,2,290,200)
node11 = node.Node(11,env,2 ,280,220 )
node12 = node.Node(12,env,2,20,200 )
node13 = node.Node(13,env,2,10,160 )
node14 = node.Node(14,env,2 ,13,183 )
node15 = node.Node(15,env,2 ,50,200 )
node16 = node.Node(16,env,2 ,29,189 )
node17 = node.Node(17,env,2 ,35,204 )
node18 = node.Node(18,env,2,31,172 )
node19 = node.Node(19,env,2,30,50 )
node20 = node.Node(20,env,2 ,150,20 )
node21 = node.Node(21,env,2,135,2 )
node22 = node.Node(22,env,2 ,165,5 )

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


net1.introduce_yourself()
print("KKKKKKKKKK")
net1.network_nodedsicovery()
graphi = gui.graphic(net1)
graphi.draw_nods()

env.run(until=30)

print(net1.nodes)

graphi.draw_neighbors()

# net1.network_inboxes()
# net1.network_outboxes()
net1.network_packet_summery()
net1.introduce_yourself()
