import simpy
import network
import node
import gui
import random

env = simpy.Environment()
net1 = network.Net(env) # create instance
net1.introduce_yourself()
# controller = node.Node(0, env, (net1.xsize)/2, (net1.xsize)/2,node_type='B' )
# net1.nodes.append(controller)
# controller.net = net1

# node1 = node.Node(1,env,2,100,200)
# node1.net = net1
# net1.nodes.append(node1)

# node2 = node.Node(2,env,2,150,150)
# node2.net = net1
# net1.nodes.append(node2)

# node3 = node.Node(3,env,2,190,193)
# node3.net = net1
# net1.nodes.append(node3)


# for i in range(20):
#     mnode = node.Node(i,env,2,random.randint(0,net1.xsize),random.randint(0,net1.ysize))
#     mnode.net= net1
#     net1.nodes.append(mnode)
net1.random_net_generator(env,net1,24)

graphi = gui.graphic(net1)
graphi.draw_nods()



env.run(until=60)

print(net1.nodes)

graphi.draw_neighbors()
print(net1.nodes)