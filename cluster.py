import network
import node
import simpy
import gui
import config
import random
import message
import time
import logger

class mycluster:
    def __init__(self,id, env ,network):
        self.id = id
        self.nodes = []
        print("\nCluster {0} is created".format(self.id))
        self.is_alive = True
        self.env = env
        self.action = env.process(self.run(env))
        self.net = network
        self.next_CH = []
        self.CH = []
        self.light = []
        self.temperature = []  
        self.logger = logger.logger()    

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def run(self,env):
        while True:
            if (self.net.superframe_num % config.cluster_rotation_period) == 0:
                self.logger.log("##### {0} {1}".format(self.net.superframe_num, env.now))
                print ("##### {0} {1}".format(self.net.superframe_num, env.now))
                self.Random_Clusterhead_Selection()
                yield self.env.timeout(config.Duration)
            #self.logger.log("cluster {0} ,CH :{1} alive {2} and average {3}".format(self.id,self.CH,self.CH.is_alive,self.average_cluster_energy()))
            #print("cluster {0} ,CH :{1} alive {2} and average {3}".format(self.id,self.CH,self.CH.is_alive,self.average_cluster_energy()))
            
            if(self.env.now % 5 == 0):
                self.Random_Clusterhead_Selection()

            if (next(reversed(self.CH.energy))< config.LOW_NODE_THRESHOLD):
                self.Random_Clusterhead_Selection()
                self.Clusterhead_Selection()
            if(self.CH.is_alive==False):
                self.Random_Clusterhead_Selection()
                self.Clusterhead_Selection()
            # print(self.id,"cluster is runing",self.env.now)
            if len(self.nodes)>7:
                print("nodes number is exceeded")
            if(self.is_alive == True):
                if(len(self.nodes)==0):
                    self.logger.log("Cluster {0} is dead@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ \n".format(self.id))
                    print("Cluster {0} is dead@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ \n".format(self.id))
                    self.is_alive = False
            yield self.env.timeout(1)

    def add_node(self, node):
        #print (self.id) # debugging...
        if(len(self.nodes )> 7):
            self.logger.log("cluster nodes is exceeded by {0}".format(node))
            print("cluster nodes is exceeded by {0}".format(node))
        node.clus==self
        node.cluster.clear()
        node.cluster.append(self)

        self.nodes.append(node)
        
        # node.TDMA_slot_number = self.nodes.index(node)
        # self.TDMA_slots += 1
        #print ("Cluster {0} has node id {1}".format(self.name,node.id))
        node.set_TDMA(self.nodes.index(node))
        
    def remove_node(self, node):
        self.nodelist.remove(node)
        # self.TDMA_slots -= 1
        
    def introduce_yourself(self):
        self.logger.log("cluster {0} has {1} with TDMA_slots {2} (introduce)\n".format(self.id,self.nodes,self.TDMA_slots))
        print("cluster {0} has {1} with TDMA_slots {2} (introduce)\n".format(self.id,self.nodes,self.TDMA_slots))


    def average_cluster_energy(self):
        average_en = 0
        if(len(self.nodes)!=0):
            for node in self.nodes:
                average_en += sum(node.energy)
            return average_en/len(self.nodes)
    
    def cluster_head_setter(self,node):

        self.CH = node
        for n in self.nodes:
            if n != node:
                n.parent_setter(node)

    def Clusterhead_Selection(self):
        maxi = max(i.energy for i in self.nodes)
        for i in self.nodes:
            if (i.energy == maxi):
                i.change_to_clusterhead()
                self.logger.log("{0} is cluster head".format(i))
                print("{0} is cluster head".format(i))
                self.cluster_head_setter(i)

    def Random_Clusterhead_Selection(self):
        prob_ch = self.net.CH_probablity()
        self.logger.log("   \n      Random_Clusterhead_Selection : cluster {0} with prob {1}".format(self.id,prob_ch))
        print("   \n      Random_Clusterhead_Selection : cluster {0} with prob {1}".format(self.id,prob_ch))
        for n in self.nodes:
            n_random = random.uniform(0,1)
            #print("random for {0} is {1}".format(n,n_random))
            if n_random < prob_ch:
                if(next(reversed(n.energy))>config.LOW_NODE_THRESHOLD):
                    self.logger.log(" <<< random for node {0} is {1} with energy {2} and average cluster energy {3}".format(n,n_random,next(reversed(n.energy)),self.average_cluster_energy()))
                    print(" <<< random for node {0} is {1} with energy {2} and average cluster energy {3}".format(n,n_random,next(reversed(n.energy)),self.average_cluster_energy()))

                    if(sum(n.energy)>self.average_cluster_energy()):
                        if(n!=self.CH):

                            self.net.ClusterHead_finder()
                            # graph = gui.graphic(self.net)
                            # graph.draw() # simple draw
                            #time.sleep(1)
                            self.logger.log("new ch is node {0}  with parent {1} and last ch was {2} with {3}".format(n,n.parent,self.CH,self.CH.parent))
                            print("new ch is node {0}  with parent {1} and last ch was {2} with {3}".format(n,n.parent,self.CH,self.CH.parent))
                            self.CH.change_CulsterHead()
                            #self.CH.parent.append(n)
                            n.parent.clear()
                            self.CH.is_CH = False
                            print("less than prob random for {0} is {1} || node energy {2} cluster energy {3}".format(n,n_random,next(reversed(n.energy)),self.average_cluster_energy()))
                            n.change_CulsterHead()
                            # n.change_TDMA(self.TDMA_slots)
                            self.cluster_head_setter(n)
                            n.cluster = self
                            self.logger.log("node {0} is CH in {1}  +  energy ++++++++++++++++++by random CH selection c ".format(n.id , self.id ,next(reversed(n.energy))))
                            print("node {0} is CH in {1}  +  energy ++++++++++++++++++by random CH selection c ".format(n.id , self.id ,next(reversed(n.energy))))
                            message2 = message.Message()
                            message2.broadcast(n,"{0} is cluster Head in {1} with TDMA ".format(n.id,self.id))

                            
                            return
    
    def cluster_average_light(self):
        temp_light = 0
        for n in self.light:
            temp_light += self.light[n]
        if len(self.light) != 0 :
            return temp_light / len(self.light)


    def cluster_average_temp(self):
        temp = 0
        for n in self.temperature:
            temp += self.temperature[n]
        if len(self.temperature) != 0 :
            return temp / len(self.temperature)