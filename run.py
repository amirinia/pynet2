#at begining you can set parameters in config file

# to run simulation you need initial ieee802154s ( just simply define nodes and addd to ieee802154)
import gui
import config
import report
import logger
import LEACH 
import clusteringKMEANS as KMEANS

# here you select if it start with statci ieee802154 or ieee802154 maker
startstatic = False
if(startstatic):
    import network as initialieee802154
else:
    import networkfrommaker as initialieee802154

# create ieee802154
net1 = initialieee802154.net1
env = initialieee802154.env


# in second step you need and algorithm
second = True
print("_____________________________Clustering Algorithm___________________________________ start\n\n")
if(second):
    KMEANS1 = KMEANS.Kmeans(env,net1,10)
else:
    LEACH1 = LEACH.LEACHC(env,net1)
print("_____________________________Clustering Algorithm___________________________________ end\n\n")



print("++++++++++++++++++++++++++++++++++++++++++++++++++")
net1.introduce_yourself()

if(config.guienabled):
    graphi = gui.graphic(net1)
    graphi.draw()

print("++++++++++++++++++++++++++++++++++++++++++++++++++ run begin ++++++++++++++++++++++++")
env.run(600)#until=config.MAX_RUNTIME)
print("++++++++++++++++++++++++++++++++++++++++++++++++++ run end ++++++++++++++++++++++++")

if(config.guienabled):
    graphi = gui.graphic(net1)
    graphi.draw()

#net1.ieee802154_packet_summery()

# for n in net1.nodes:
#     print(n,n.TDMA,n.is_CH,n.cluster,"   ",n.distance)


# print(net1.clusters)
# print(net1.clusterheads)

# print(net1.nodes[0].inbox)
net1.introduce_yourself()   

# net1.ieee802154_outboxes()
# net1.ieee802154_inboxes()


net1.ieee802154_packet_summery()
#net1.ieee802154_optimize()
#report.plotpacket()
#report.plotenergy()
