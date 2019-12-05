import numpy as np 
import random 
import pandas as pd
import staticnet as initialnetwork
import gui
import config
import report
import logger

def run(x):
    df = pd.DataFrame(columns=['pop','energy','duration','lost','dead'])

    config.TDMA_duration = x[0]
    config.CSMA_duration = x[1]
    config.Inactive_duration = x[2]
    if x[3] ==0:
        config.Multiframe_state = True
    else:
        config.Multiframe_state = False
   
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

    #report.plotenergy()
    #report.plotpacket()

    a = net1.network_optimize()
    #df = df.append(pd.Series([x,a[0],a[1],a[2],a[3]], index=df.columns), ignore_index=True)

    return a



#print(run([  7,   8, 192,   0]))
















# def f(chromosome):
#     print("ch",chromosome)
#     return 0

# def create_random():
#         t1 = np.random.randint(low=4, high=7, size=1)
#         t2 = np.random.randint(low=1, high=9, size=1)
#         t3 = np.random.randint(low=0, high= 240 - t1 -t2, size=1)
#         b1 = np.random.choice([0, 1])
#         t = np.concatenate((t1, t2, t3, b1), axis=None)
#         #print(t)
#         return t
# List = []
# f(create_random())