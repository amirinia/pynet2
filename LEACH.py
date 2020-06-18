import random
import cluster
import message
import network
import node
import simpy
import logger
import config
import gui

class LEACHC:
    def __init__(self,env, network):
        self.env = env
        self.network = network
        self.logger = logger.logger()
        self.clusterheads = []
        self.clusters = []
        self.global_cluster_fromation(env)
        self.initial = False
        self.action = env.process(self.run(env))

    def run(self,env): #steady pahse
        while True:
            # if(not self.initial):# initial phase
            #     print("LEACH intial phase...")
            #     self.initial = True
            #     self.global_cluster_fromation(env)


            if(self.env.now % 500 == 0):
                for c in self.clusters:
                    self.Random_Clusterhead_SelectionCluster(c)
                print("R buz 1000")
            #yield self.env.process(self.Random_Clusterhead_Selection(10))
            yield self.env.timeout(1)

    def global_cluster_fromation(self,env):
        for node in self.network.nodes:
            tempmessage = "beacon on LEACH from {0}".format(node)
            message1 = message.Message(tempmessage)
            message1.broadcast(node,tempmessage)
            if(len(node.neighbors)!=0):

                if(node.energy >= max(neighbor.energy for neighbor in node.neighbors)):
                    node.change_CulsterHead()
                    mycluster1 = cluster.mycluster(node.id,env,self.network)
                    for n in node.neighbors:
                        mycluster1.add_node(n)
                    mycluster1.CH = node
                    node.set_TDMA(len(mycluster1.nodes))
                    # node.change_TDMA(mycluster1.TDMA_slots)
                    self.logger.log("{0} is CH in {1} with {2} energy ++++++++++++++++++\n".format(node.id , mycluster1.id,str(node.energy) ) )
                    print("{0} is CH in {1} with {2} energy ++++++++++++++++++\n".format(node.id , mycluster1.id,str(node.energy) ) )
                    message2 = message.Message()
                    message2.broadcast(node,"node {0} is cluster Head in {1} with TDMA ".format(node.id,mycluster1.id))
                    
                    self.network.add_cluster(mycluster1)
                    self.clusters.append(mycluster1)
                    self.network.clusterheads.append(node)
                    self.clusterheads.append(node)
                    #yield self.env.timeout(1)

    def Random_Clusterhead_Selection(self,env,network):
        self.logger.log("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH \n")
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
            
 

    def ClusterHead_finder(self):# pass network to it and it sets the BS neighbors who are CH
        self.network.clusterheads.clear()
        self.clusterheads.clear()

        for n in self.network.nodes:
            if(n.is_alive==True):
                if (n.is_CH == True):
                    #self.network.clusterheads.append(n)
                    self.network.clusterheads.append(n)
                    self.network.clusterheads =  list(dict.fromkeys(self.clusterheads)) 
                    self.clusterheads.append(n)
                    self.clusterheads =  list(dict.fromkeys(self.clusterheads)) # remove duplicates
        # print("clusterheads are {0} in network  \n".format(self.clusterheads))

    def CH_probablity(self):# send network to this
        if(len(self.clusters)==0):
            print("there is no cluster to cal CH_prob")
        return float(len(self.clusters))/float(len(self.network.nodes))



    def Clusterhead_Selection(self):
        maxi = max(i.energy for i in self.nodes)
        for i in self.nodes:
            if (i.energy == maxi):
                i.change_to_clusterhead()
                self.logger.log("{0} is cluster head".format(i))
                print("{0} is cluster head".format(i))
                self.cluster_head_setter(i)

    def Random_Clusterhead_SelectionCluster(self,cluster):
        prob_ch =  self.CH_probablity()
        cluster.logger.log("   \n      Random_Clusterhead_Selection : cluster {0} with prob {1}".format(cluster.id,prob_ch))
        print("   \n      Random_Clusterhead_Selection : cluster {0} with prob {1}".format(cluster.id,prob_ch))
        for n in cluster.nodes:
            n_random = random.uniform(0,1)
            #print("random for {0} is {1}".format(n,n_random))
            if n_random < prob_ch:
                if(next(reversed(n.energy))>config.LOW_NODE_THRESHOLD):
                    cluster.logger.log(" <<< random for node {0} is {1} with energy {2} and average cluster energy {3}".format(n,n_random,next(reversed(n.energy)),cluster.average_cluster_energy()))
                    print(" <<< random for node {0} is {1} with energy {2} and average cluster energy {3} low threshold {4}".format(n,n_random,next(reversed(n.energy)),cluster.average_cluster_energy(),config.LOW_NODE_THRESHOLD))
                    print(n.is_CH, " .neighbors ",n.neighbors)
                    if(sum(n.energy)> cluster.average_cluster_energy()):
                        if(n!=cluster.CH):
                            
                            self.ClusterHead_finder()

                            cluster.logger.log("new ch is node {0}  with parent {1} and last ch was {2} with {3}".format(n,n.parent,cluster.CH,cluster.CH.parent))
                            print("new ch is node {0}  with parent {1} and last ch was {2} with {3}".format(n,n.parent,cluster.CH,cluster.CH.parent))
                            cluster.CH.change_CulsterHead()
                            #cluster.CH.parent.append(n)
                            n.parent.clear()
                            cluster.CH.is_CH = False
                            print("less than prob random for {0} is {1} || node energy {2} cluster energy {3}".format(n,n_random,next(reversed(n.energy)),cluster.average_cluster_energy()))
                            n.change_CulsterHead()
                            # n.change_TDMA(cluster.TDMA_slots)
                            cluster.cluster_head_setter(n)
                            n.cluster = cluster
                            cluster.logger.log("node {0} is CH in {1}  +  energy ++++++++++++++++++by random CH selection c ".format(n.id , cluster.id ,next(reversed(n.energy))))
                            print("node {0} is CH in {1}  +  energy ++++++++++++++++++by random CH selection c ".format(n.id , cluster.id ,next(reversed(n.energy))))
                            message2 = message.Message()
                            message2.broadcast(n,"{0} is cluster Head in {1} with TDMA ".format(n.id,cluster.id))
                            self.ClusterHead_finder()
                            graph = gui.graphic(cluster.net)
                            graph.draw() # simple draw
                            #time.sleep(1)