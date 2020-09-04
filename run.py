#at begining you can set parameters in config file

# to run simulation you need initial ieee802154s ( just simply define nodes and addd to ieee802154)
import gui
import config
import report
import logger
import LEACH 
import clusteringKMEANS as KMEANS
import pickle
import simpy
import ieee802154
from node import Node


# here you select if it start with statcinet or network maker
startstatic = True
if(startstatic):
    import network as net
else:
    import networkfrommaker as net


# import ieee802154
ieee1 = net.ieee1
env = net.env


# in second step you need and algorithm
second = False
if config.printenabled:
    print("_____________________________Clustering Algorithm___________________________________ start\n\n")
if(second):
    KMEANS1 = KMEANS.Kmeans(env,ieee1,10)
else:
    LEACH1 = LEACH.LEACHC(env,ieee1)
if config.printenabled:
    print("_____________________________Clustering Algorithm___________________________________ end\n\n")


if config.printenabled:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
ieee1.introduce_yourself()

if(config.guienabled):
    graphi = gui.graphic(ieee1)
    graphi.draw_neighbors()
    graphi.draw()
if config.printenabled:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++ run begin ++++++++++++++++++++++++")
env.run(until=config.MAX_RUNTIME)
if config.printenabled:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++ run end ++++++++++++++++++++++++")

if(config.guienabled):
    graphi = gui.graphic(ieee1)
    graphi.draw()

#ieee1.ieee802154_packet_summery()

# for n in ieee1.nodes:
#     print(n,n.TDMA,n.is_CH,n.cluster,"   ",n.distance)


# print(ieee1.clusters)
# print(ieee1.clusterheads)

# print(ieee1.nodes[0].inbox)
ieee1.introduce_yourself()   

# ieee1.ieee802154_outboxes()
# ieee1.ieee802154_inboxes()


#ieee1.ieee802154_packet_summery()
ieee1.ieee802154_optimize()
#report.plotpacket()
#report.plotenergy()