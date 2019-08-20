#at begining you can set parameters in config file
import gui
import simpy
import network
import node
import KMEANS

# to run simulation you need initial networks ( just simply define nodes and addd to network or use random generator)
env = simpy.Environment()
net1 = network.Net(env)
net1.random_net_generator(env,net1,40)
net1.introduce_yourself()
graphi = gui.graphic(net1)
graphi.draw_nods()


# in second step you need and algorithm
print("_____________________________Algorithm___________________________________ start\n\n")
KMEANS.Kmeans(net1,7)
print("_____________________________Algorithm___________________________________ end\n\n")

# graphi.draw_clusters()
net1.cluster_formation()
net1.introduce_yourself()

# for n in net1.nodes:
#     print(n,n.neighbors)
#     if len(n.parent) != 0:
#         print(n,next(reversed(n.parent)))

print("++++++++++++++++++++++++++++++++++++++++++ run begin ++++++++++++++++++++++++")
env.run(until=1)#config.MAX_RUNTIME)
print("++++++++++++++++++++++++++++++++++++++++++ run end ++++++++++++++++++++++++")

net1.network_packet_summery()


# for n in net1.nodes:
#     print(n,n.neighbors)
#     if len(n.parent) != 0:
#         print(n,next(reversed(n.parent)))


for n in net1.nodes:
    print(n,n.is_CH,n.distance)
graphi.draw_neighbors()

net1.introduce_yourself()
net1.network_outboxes()
net1.network_inboxes()