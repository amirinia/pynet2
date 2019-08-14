import network
import node
import simpy

class mycluster:
    def __init__(self,id, env ,network):
        self.id = id
        self.nodes = []
        print("\nCluster {0} is created".format(self.id))
        self.is_alive = True
        self.env = env
        self.action = env.process(self.run(env))
        self.network = network
        self.next_CH = []
        self.CH = []      

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def run(self,env):
        print(self.id,"cluster is runing",self.env.now)
        if len(self.nodes)>7:
            print("nodes number is exceeded")
        if(self.is_alive == True):
            if(len(self.nodes)==0):
                print("Cluster {0} is dead@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ \n".format(self.id))
                self.is_alive = False
        yield self.env.timeout(1)

    def add_node(self, node):
        #print (self.id) # debugging...
        if(len(self.nodes )> 7):
            print("cluster nodes is exceeded by",node)
        node.clus==self
        node.cluster.append(self)

        self.nodes.append(node)
        
        # node.TDMA_slot_number = self.nodes.index(node)
        # self.TDMA_slots += 1
        #print ("Cluster {0} has node id {1}".format(self.name,node.id))
        node.TDMA = self.nodes.index(node)
        
    def remove_node(self, node):
        self.nodelist.remove(node)
        # self.TDMA_slots -= 1
        
    def introduce_yourself(self):
        print("cluster {0} has {1} with TDMA_slots {2} (introduce)\n".format(self.id,self.nodes,self.TDMA_slots))


    def average_cluster_energy(self):
        average_en = 0
        if(len(self.nodes)!=0):
            for node in self.nodelist:
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
                print(i,"is cluster head")
                self.cluster_head_setter(i)