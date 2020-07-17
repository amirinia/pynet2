import random
import cluster
import message
import ieee802154
import node
import simpy
import logger
import config
import gui

class LEACHC:
    def __init__(self,env, ieee802154):
        self.env = env
        self.ieee802154 = ieee802154
        self.logger = logger.logger()
        self.clusterheads = []
        self.clusters = []
        self.rotation_time = 500
        self.notclustered = []
        self.initial = False

        self.cluster_fromation_area(env,self.ieee802154.nodes)
        self.action = env.process(self.run(env))


    def run(self,env): #steady pahse
        while True:
            # if(not self.initial):# initial phase
            #     print("LEACH intial phase...")
            #     self.initial = True
            #     self.global_cluster_fromation(env)


            if(self.env.now % self.rotation_time == 50):
                for c in self.clusters:
                    self.Random_Clusterhead_SelectionCluster(c)
                if config.printenabled:
                    print("R buz 1000")
            #yield self.env.process(self.Random_Clusterhead_Selection(10))
            yield self.env.timeout(1)

    def cluster_fromation(self,env ,nodes):

        for node in nodes:
            tempmessage = "beacon on LEACH from {0}".format(node)
            message1 = message.Message(tempmessage)
            message1.broadcast(node,tempmessage,node.neighbors)
            if(len(node.neighbors)!=0 and node.id !=0):

                if(node.energy >= max(neighbor.energy for neighbor in node.neighbors)):
                    node.change_CulsterHead()
                    mycluster1 = cluster.mycluster(node.id,env,self.ieee802154)
                    mycluster1.add_node(node) # add ch to node list
                    for n in node.neighbors: # add neighbor of CH to cluster
                        if(n.id != 0):
                            mycluster1.add_node(n)
                    mycluster1.cluster_head_setter(n)
                    mycluster1.CH = node
                    self.logger.log("{0} is CH in cluster {1} with {2}  ++++++++++++++++++\n".format(node.id , mycluster1.id,str(mycluster1.nodes) ) )
                    if config.printenabled:
                        print("{0} is CH in cluster {1} with {2}  ++++++++++++++++++\n".format(node.id , mycluster1.id,str(mycluster1.nodes) ) )
                    message2 = message.Message()
                    message2.broadcast(node,"node {0} is cluster Head in {1} with TDMA ".format(node.id,mycluster1.id),node.neighbors)
                    
                    self.ieee802154.add_cluster(mycluster1)
                    self.clusters.append(mycluster1)
                    self.ieee802154.clusterheads.append(node)
                    self.clusterheads.append(node)
                    #yield self.env.timeout(1)
        
        for node in self.ieee802154.nodes:
            if (node.is_CH == False):
                if (len(node.parent) == 0):
                    self.notclustered.append(node)

        if(len(self.notclustered) != 0):
            if config.printenabled:
                print("these are not clustered ",self.notclustered)

    def cluster_fromation_area(self,env ,nodes):
        mycluster1 = cluster.mycluster(1,env,self.ieee802154)
        mycluster2 = cluster.mycluster(2,env,self.ieee802154)
        mycluster3 = cluster.mycluster(3,env,self.ieee802154)
        mycluster4 = cluster.mycluster(4,env,self.ieee802154)
        mycluster5 = cluster.mycluster(5,env,self.ieee802154)
        mycluster6 = cluster.mycluster(6,env,self.ieee802154)
        mycluster7 = cluster.mycluster(7,env,self.ieee802154)
        mycluster8 = cluster.mycluster(8,env,self.ieee802154)
        mycluster9 = cluster.mycluster(9,env,self.ieee802154)

        for node in nodes:
            if(node.id !=0):
                if node.x <=100:
                    if node.y <=100:
                        mycluster1.add_node(node) # add ch to node list
                    if node.y <=200 and node.y >100:
                        mycluster2.add_node(node) # add ch to node list                    
                    if node.y <=300 and node.y > 200:
                        mycluster3.add_node(node) # add ch to node list
                        
                if node.x > 100 and node.x <=200:
                    #print(node.id, node.x,node.y)
                    if node.y <=100:
                        mycluster4.add_node(node) # add ch to node list
                        #print(node.id, node.x)
                    if node.y <=200 and node.y >100:
                        mycluster5.add_node(node) # add ch to node list 
                        #print(node.id, node.x)
                    if node.y <=300 and node.y > 200:
                        mycluster6.add_node(node) # add ch to node list
                        #print(node.id, node.x)

                if node.x > 200 and node.x <=300:
                    #print(node.id, node.x)
                    if node.y <=100:
                        mycluster7.add_node(node) # add ch to node list
                    if node.y <=200 and node.y >100:
                        mycluster8.add_node(node) # add ch to node list                    
                    if node.y <=300 and node.y > 200:
                        mycluster9.add_node(node) # add ch to node list

        self.clusters.append(mycluster1)
        self.clusters.append(mycluster2)
        self.clusters.append(mycluster3)
        self.clusters.append(mycluster4)
        self.clusters.append(mycluster5)
        self.clusters.append(mycluster6)
        self.clusters.append(mycluster7)
        self.clusters.append(mycluster8)
        self.clusters.append(mycluster9)
        for c in self.clusters:
            for node in c.nodes:
                if(node.energy >= max(neighbor.energy for neighbor in c.nodes)):

                    c.cluster_head_setter(node)
                    c.CH = node
                    node.change_CulsterHead()
                    self.logger.log("{0} is CH in cluster {1} with {2}  ++++++++++++++++++ area\n".format(node.id , c.id,str(c.nodes) ) )
                    if config.printenabled:
                        print("{0} is CH in cluster {1} with {2}  ++++++++++++++++++ is CH {3} area \n".format(node.id , c.id,str(c.nodes),node.is_CH ) )
                    message2 = message.Message()
                    message2.broadcast(node,"node {0} is cluster Head in {1} with TDMA ".format(node.id,c.id),node.neighbors)
                    self.ieee802154.clusterheads.append(node)
                    self.clusterheads.append(node)
            self.ieee802154.add_cluster(c)
            #self.Random_Clusterhead_SelectionCluster(c)


        for node in self.ieee802154.nodes:
            #print(node.id, node.is_CH)
            if (node.is_CH == False):
                if (len(node.parent) == 0):
                    self.notclustered.append(node)

        if(len(self.notclustered) != 0):
            if config.printenabled:    
                print("these are not clustered area ",self.notclustered)



    def Random_Clusterhead_Selection_steady(self,env):
        yield self.env.timeout(7)
        if config.printenabled:
            print("Random_Clusterhead_Selection_steady")
            
 

    def ClusterHead_finder(self):# pass ieee802154 to it and it sets the BS neighbors who are CH
        self.ieee802154.clusterheads.clear()
        self.clusterheads.clear()

        for n in self.ieee802154.nodes:
            if(n.is_alive==True):
                if (n.is_CH == True and n.id != 0):
                    #self.ieee802154.clusterheads.append(n)
                    self.ieee802154.clusterheads.append(n)
                    self.ieee802154.clusterheads =  list(dict.fromkeys(self.clusterheads)) 
                    self.clusterheads.append(n)
                    self.clusterheads =  list(dict.fromkeys(self.clusterheads)) # remove duplicates
        # print("clusterheads are {0} in ieee802154  \n".format(self.clusterheads))

    def CH_probablity(self):# send ieee802154 to this
        if(len(self.clusters)==0):
            if config.printenabled:
                print("there is no cluster to cal CH_prob")
        return float(len(self.clusters))/float(len(self.ieee802154.nodes))



    def Clusterhead_Selection(self):
        maxi = max(i.energy for i in self.nodes)
        for i in self.nodes:
            if (i.energy == maxi and i.id !=0):
                i.change_to_clusterhead()
                self.logger.log("{0} is cluster head".format(i))
                if config.printenabled:
                    print("{0} is cluster head".format(i))
                self.cluster_head_setter(i)

    def Random_Clusterhead_SelectionCluster(self,cluster):
        prob_ch =  self.CH_probablity()
        cluster.logger.log("   \n      Random_Clusterhead_Selection : cluster {0} with prob {1}".format(cluster.id,prob_ch))
        if config.printenabled:
            print("   \n      Random_Clusterhead_Selection : cluster {0} with prob {1}".format(cluster.id,prob_ch))
        av = cluster.average_cluster_energy()
        if config.printenabled:
            print("av enargy = ",av ," cluster nodes ",cluster.nodes)
        toplist = []
        for n in cluster.nodes:
            #print(n.id," en: ",next(reversed(n.energy)))
            if(next(reversed(n.energy)) >= av and n.id != 0):
                toplist.append(n)
        if config.printenabled:
            print("toplist",toplist)
        
        for n in toplist:
            if(n == self.findmaxenergy(toplist)):
                random_node = random.choice(cluster.nodes)
                if(random_node.id == n.id):
                    if config.printenabled:
                        print(n.id," ",n.is_CH, " .neighbors ",n.neighbors," energy : ",next(reversed(n.energy)), " r.id ",random_node.id)

                #print("random for {0} is {1}".format(n,n_random))
                n_random = random.uniform(0,1)
            
                if n_random < prob_ch:
                
                    cluster.logger.log(" <<< random for node {0} is {1} with energy {2} and average cluster energy {3}".format(n,n_random,next(reversed(n.energy)),cluster.average_cluster_energy()))
                    if config.printenabled:
                        print("at ",self.env.now," <<< random for node {0} is {1} with energy {2} and average cluster energy {3} low threshold {4}".format(n,n_random,next(reversed(n.energy)),cluster.average_cluster_energy(),config.LOW_NODE_THRESHOLD))
                    if(sum(n.energy)> cluster.average_cluster_energy()):
                        if(n!=cluster.CH):
                            
                            #self.ClusterHead_finder()

                            cluster.logger.log("new ch is node {0}  with parent {1} and last ch was {2} with {3}".format(n,n.parent,cluster.CH,cluster.CH.parent))
                            if config.printenabled:
                                print("new ch is node {0}  with parent {1} and last ch was {2} with {3}".format(n,n.parent,cluster.CH,cluster.CH.parent))
                            cluster.CH.change_CulsterHead()
                            #cluster.CH.parent.append(n)
                            n.parent.clear()
                            cluster.CH.is_CH = False
                            #print("less than prob random for {0} is {1} || node energy {2} cluster energy {3}".format(n,n_random,next(reversed(n.energy)),cluster.average_cluster_energy()))
                            n.change_CulsterHead()
                            # n.change_TDMA(cluster.TDMA_slots)
                            cluster.cluster_head_setter(n)
                            n.cluster = cluster
                            cluster.logger.log("node {0} is CH in {1}  +  energy ++++++++++++++++++by random CH selection c ".format(n.id , cluster.id ,next(reversed(n.energy))))
                            if config.printenabled:
                                print("node {0} is CH in {1}  +  energy ++++++++++++++++++by random CH selection c ".format(n.id , cluster.id ,next(reversed(n.energy))))
                            message2 = message.Message()
                            message2.broadcast(n,"{0} is cluster Head in {1} with TDMA ".format(n.id,cluster.id),n.neighbors)
                            self.ClusterHead_finder()
                            if(config.guienabled):
                                graph = gui.graphic(cluster.net)
                                graph.draw() #  draw
                            #time.sleep(1)
                            
                            return # it 
    
    def findmaxenergy(self,nodelist):
        energylist = []
        for n in nodelist:
            energylist.append(next(reversed(n.energy)))
        
        for n in nodelist:
            if (max(energylist) == next(reversed(n.energy))):
                #print(n.id, " has max energy " ,max(energylist))
                return n
