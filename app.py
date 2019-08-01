import simpy
import network
import node
import gui

env = simpy.Environment()
net1 = network.Net(env) # create instance

# controller = node.Node(0, env, (net1.xsize)/2, (net1.xsize)/2,node_type='B' )
# net1.nodes.append(controller)
# controller.net = net1

node1 = node.Node(1,env)
node1.net = net1

node2 = node.Node(2,env,)
node2.net = net1
graphi = gui.graphic(net1)
graphi.draw_nods()

print(node1.x)
env.run(until=40)