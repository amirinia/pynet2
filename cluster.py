import network
import node
import simpy
import gui
import config
import random
import message
import time
import logger
import LEACH
import pickle

class mycluster:
    def __init__(self,id, env ,network):
        self.id = id
        self.nodes = []
        self.is_alive = True
        self.env = env
        self.action = env.process(self.run(env))
        self.net = network
        self.next_CH = []
        self.CH = node.Node
        self.light = []
        self.temperature = []  
        self.logger = logger.logger()
        self.saveClusterPos()    
        print("\nCluster {0} is created".format(self.id))
        


    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)


    def saveClusterPos(self): # save nodes position
        pos =[]
        for n in self.nodes:
            pos.append([n.x,n.y])
        pickle.dump(pos, file = open("posCluster{0}.pickle".format(self.id), "wb"))

    def run(self,env):
        while True:
            if (self.net.superframe_num % config.cluster_rotation_period) == 0:
                self.logger.log("##### {0} {1}".format(self.net.superframe_num, env.now))
                print ("##### {0} {1}".format(self.net.superframe_num, env.now))
                #self.Random_Clusterhead_Selection()
                yield self.env.timeout(config.Duration)
            #self.logger.log("cluster {0} ,CH :{1} alive {2} and average {3}".format(self.id,self.CH,self.CH.is_alive,self.average_cluster_energy()))
            #print("cluster {0} ,CH :{1} alive {2} and average {3}".format(self.id,self.CH,self.CH.is_alive,self.average_cluster_energy()))
            
            

            if(self.CH.is_alive == False):
                #self.Random_Clusterhead_Selection()
                #self.Clusterhead_Selection()
                print("Cluster head is buz dead inside cluster")
                for n in self.nodes:
                    if (n.is_alive == True):
                        self.cluster_head_setter(n)
                        return


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
        node.cluster = []
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
                average_en += (next(reversed(node.energy)))
            return average_en/len(self.nodes)
    
    def cluster_head_setter(self,node):
        if(node.is_alive):
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

