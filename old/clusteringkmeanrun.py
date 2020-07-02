#at begining you can set parameters in config file
import gui
import simpy
import ieee802154
import node
import clusteringKMEANS as KMEANS

# to run simulation you need initial ieee802154s ( just simply define nodes and addd to ieee802154 or use random generator)
#import networkfrommaker as initialieee802154
# here you select if it start with statci ieee802154 or ieee802154 maker
startstatic = False
if(startstatic):
    import network as initialieee802154
else:
    import networkfrommaker as initialieee802154


net1 = initialieee802154.net1
env = initialieee802154.env
#net1.random_net_generator(env,net1,40)
# net1.introduce_yourself()
# graphi = gui.graphic(net1)
# graphi.draw_nods()


# in second step you need and algorithm
print("_____________________________Algorithm___________________________________ start\n\n")
k1 = KMEANS.Kmeans(env,net1,7)
print("_____________________________Algorithm___________________________________ end\n\n")

# graphi.draw_clusters()
#net1.cluster_formation()
net1.introduce_yourself()

# for n in net1.nodes:
#     print(n,n.neighbors)
#     if len(n.parent) != 0:
#         print(n,next(reversed(n.parent)))

print("++++++++++++++++++++++++++++++++++++++++++ run begin ++++++++++++++++++++++++")
env.run(until=100)#config.MAX_RUNTIME)
print("++++++++++++++++++++++++++++++++++++++++++ run end ++++++++++++++++++++++++")

#net1.ieee802154_packet_summery()


# for n in net1.nodes:
#     print(n,n.neighbors)
#     if len(n.parent) != 0:
#         print(n,next(reversed(n.parent)))



#graphi.draw_neighbors()

net1.introduce_yourself()
#net1.ieee802154_outboxes()
#net1.ieee802154_inboxes()