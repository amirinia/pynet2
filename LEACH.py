import random
import cluster
import message
import network
import node
import simpy


class LEACHC:
    def __init__(self,env, network):
        self.env = env
        self.network = network

    def global_cluster_fromation(self,env):
        for node in self.network.nodes:
            if(len(node.neighbors)!=0):

                if(node.energy >= max(neighbor.energy for neighbor in node.neighbors)):
                    # node.change_CulsterHead()
                    mycluster1 = cluster.mycluster(node.id,env,self.network)
                    for n in node.neighbors:
                        mycluster1.add_node(n)
                    mycluster1.CH =node
                    # node.change_TDMA(mycluster1.TDMA_slots)
                    print("{0} is CH in {1} with {2}  energy ++++++++++++++++++\n".format(node.id , mycluster1.id,str(node.energy) ) )
                    message2 = message.Message()
                    message2.broadcast(node,"node {0} is cluster Head in {1} with TDMA ".format(node.id,mycluster1.id))
                    
                    self.network.add_cluster(mycluster1)
                    self.network.clusterheads.append(node)


    def Random_Clusterhead_Selection(self,env,network):
        print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH \n")
            #initial clusters
        self.global_cluster_fromation(env)
        # yield self.env.timeout(1)
        # try:
        #     yield self.env.process(self.Random_Clusterhead_Selection_steady(env))
        # except simpy.Interrupt:
        #     print("inter")

        # prob_ch = self.network.CH_probablity()
        # print("probib {0}".format(prob_ch))
        # print(network.clusters)
        # print(self.network.clusters)

    def Random_Clusterhead_Selection_steady(self,env):
        yield self.env.timeout(7)
        print("Random_Clusterhead_Selection_steady")
            
    def local_cluster_formation():
        pass