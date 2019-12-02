#at begining you can set parameters in config file

# to run simulation you need initial networks ( just simply define nodes and addd to network)
import staticnet as initialnetwork
import gui
import config
import report
import logger

#initialnetwork.net1.introduce_self()
net1 = initialnetwork.net1
env = initialnetwork.env
graphi = gui.graphic(net1)


# in second step you need and algorithm
#logger.logger.log(str("__________________________LEACH___________________________________________ start"))
print("__________________________LEACH___________________________________________ start\n\n")
import LEACH 

LEACH1 = LEACH.LEACHC(env,net1)
#LEACH1.global_cluster_fromation(env)
LEACH1.Random_Clusterhead_Selection(env,net1)
#logger.logger.log(str("__________________________LEACH___________________________________________ end"))
print("__________________________LEACH___________________________________________ end\n\n")


print("++++++++++++++++++++++++++++++++++++++++++++++++++")
net1.introduce_yourself()
graphi.draw()
#logger.logger.log(str("++++++++++++++++++++++++++++++++++++++++++++++++++ run begin ++++++++++++++++++++++++"))
print("++++++++++++++++++++++++++++++++++++++++++++++++++ run begin ++++++++++++++++++++++++")

env.run(until=config.MAX_RUNTIME)
#logger.logger.log(str("++++++++++++++++++++++++++++++++++++++++++++++++++ run end ++++++++++++++++++++++++"))
print("++++++++++++++++++++++++++++++++++++++++++++++++++ run end ++++++++++++++++++++++++")


net1.network_packet_summery()

# for n in net1.nodes:
#     print(n,n.TDMA,n.is_CH,n.cluster,"   ",n.distance)


# print(net1.clusters)
# print(net1.clusterheads)

# print(net1.nodes[0].inbox)
net1.introduce_yourself()   

# net1.network_outboxes()
# net1.network_inboxes()

report.plotenergy()
report.plotpacket()

