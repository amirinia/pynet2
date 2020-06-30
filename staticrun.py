#at begining you can set parameters in config file

# to run simulation you need initial networks ( just simply define nodes and addd to network)
import gui
import config
import report
import logger
import LEACH 
import clusteringKMEANS as KMEANS

# here you select if it start with statci network or network maker
startstatic = False
if(startstatic):
    import staticnet as initialnetwork
else:
    import staticnetfrommaker as initialnetwork

# create network
net1 = initialnetwork.net1
env = initialnetwork.env


# in second step you need and algorithm
second = False
print("_____________________________Clustering Algorithm___________________________________ start\n\n")
if(second):
    KMEANS1 = KMEANS.Kmeans(env,net1,10)
else:
    LEACH1 = LEACH.LEACHC(env,net1)
print("_____________________________Clustering Algorithm___________________________________ end\n\n")



print("++++++++++++++++++++++++++++++++++++++++++++++++++")
net1.introduce_yourself()
graphi = gui.graphic(net1)
graphi.draw()

print("++++++++++++++++++++++++++++++++++++++++++++++++++ run begin ++++++++++++++++++++++++")
env.run(600)#until=config.MAX_RUNTIME)
print("++++++++++++++++++++++++++++++++++++++++++++++++++ run end ++++++++++++++++++++++++")


#net1.network_packet_summery()

# for n in net1.nodes:
#     print(n,n.TDMA,n.is_CH,n.cluster,"   ",n.distance)


# print(net1.clusters)
# print(net1.clusterheads)

# print(net1.nodes[0].inbox)
net1.introduce_yourself()   

# net1.network_outboxes()
# net1.network_inboxes()


net1.network_packet_summery()
#net1.network_optimize()
#report.plotpacket()
#report.plotenergy()
