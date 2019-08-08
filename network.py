import simpy
import random
import node
import config
import math
import RSSI
import cluster
"""
"""

class Net():
    def __init__(self,env,xsize=config.AREA_WIDTH,ysize=config.AREA_LENGTH):
        self.env = env
        self.action = env.process(self.run())
        self.clock = ["CSMA"]
        self.nodes = []
        self.clusters = []
        self.xsize = xsize
        self.ysize = ysize
        #add controller
        controller = node.Node(0, self.env,4, (self.xsize)/2, (self.ysize)/2,node_type='B' ,power_type=0)
        self.nodes.append(controller)
        controller.net = self
    
    def run(self):
        
        counter = 0
        initial = False
        while True:
            if(initial == False):
                try:
                    yield self.env.process(self.initialization(10))
                except simpy.Interrupt:
                    print('Was interrupted.CSMA')
                initial = True

            counter +=1
            print('\n New Superframe is began CSMA at %d number %d\n' % (self.env.now ,counter))
            CSMA_duration = 9

            try:
                yield self.env.process(self.CSMA(CSMA_duration))
            except simpy.Interrupt:
                print('Was interrupted.CSMA')

            #print('TDMA at %d\n' % env.now)
            TDMA_duration = 7

            try:
                yield self.env.process(self.TDMA(TDMA_duration))
            except simpy.Interrupt:
                print('Was interrupted.TDMA')

            #print('INACTIVE at %d\n' % env.now)
            inactive_duration = 14
            for i in range(inactive_duration):
                self.clock.clear()
                self.clock.append("INACTIVE")
                print("at %d inactive network" %self.env.now)
                yield self.env.timeout(1)
            # self.network_nodedsicovery()
            # print(self.nodes)
            # print("net discovery")
    
    def initialization(self,duration):
        print('initial')
        print("Inititial network %d nods at %d"%(len(self.nodes),self.env.now))
        yield self.env.timeout(duration)


    def TDMA(self,duration):
        for i in range(duration):
            self.clock.clear()
            self.clock.append("TDMA")
            print("at {0} TDMA {1}".format(self.env.now,(self.env.now % config.TDMA_duration)))
            yield self.env.timeout(1)

    def CSMA(self,duration):
        for i in range(duration):
            self.clock.clear()
            self.clock.append("CSMA")
            #print("CSMA",env.now)
            yield self.env.timeout(1)


    def random_net_generator(self,env,network,node_number):
        print("Random network is generated with %d nodes\n"%node_number)
        for i in range(node_number):
                mnode = node.Node(i+1,env ,random.random(),random.randint(0,self.xsize),random.randint(0,self.ysize))
                mnode.net= self
                self.nodes.append(mnode)
        self.network_nodedsicovery()
        #print("random")

    def add_node(self, node):
        #print (self.id) # debugging...
        self.nodes.append(node)
        node.network = self


    def network_nodedsicovery(self,distance = config.TX_RANGE):
        print("++++++++++++++++++++ network Table Discovery Begins %d meters ++++++++++++++++++++++++++++"%config.TX_RANGE)
        for n in self.nodes:
            print("Neighbors Table discovery for {0} is :".format(str(n.id)))
            for n1 in self.nodes:
                #print(math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2)))
                if(distance > math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2))):
                    if(n!=n1):
                        if n1 not in n.neighbors:
                            n.neighbors.append(n1)
                            print("{0} <=> {1} d= {2} rssi {3}".format(str(n.id) , str(n1.id) , round(math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2)),2),round(RSSI.RSSI_nodes(n,n1)),4))
        print("+++++++++++++++++++++ network Table Discovery Ends +++++++++++++++++++++++++++++++ \n")


    def distance(self, node ,node1):
        return math.sqrt(((node.x-node1.x)**2)+((node.y-node1.y)**2))


    def network_inboxes(self):
        print("\nInboxes are shown: ")
        for n in self.nodes:
            print("Inbox {0} has {1} \n".format(str(n.id) ,str(n.inbox)))

    def network_outboxes(self):
        print("\nOutboxes are shown: ")
        for n in self.nodes:
            print("Outbox {0} has {1} \n".format(str(n.id) ,str(n.outbox)))

    def introduce_yourself(self):
        print("****************************Begin of introduce network" )
        # print("Network {0} with {1} node number with size {2} {3} and have {4} clusters".format(self.name,len(self.nodelist),self.xsize,self.ysize,len(self.clusterheads)))
        #print("New network is created : {0} with {1} node number ".format(self.name,self.nodelist.count))
        for x in self.nodes:
            if len(x.parent) == 0:
                print("{0} is alive: {5} with energy : {1} with position {2} {3} ; CH is {4}".format(x.id , x.power ,str(x.x) , str(x.y) ,str(x.parent),x.is_alive))

            if len(x.parent) != 0:
                print("{0} is alive: {5} with energy : {1} with position {2} {3} ; CH is {4}".format(x.id , x.power ,str(x.x) , str(x.y) ,str(next(reversed(x.parent))),x.is_alive))
        print("==============================Clusters===============================")
        # for c in self.clusters:
        #     print("{0} is alive: {5} with energy : {1} with nodes {2} ; TDMA: {3} ; CH is {4}".format(c.name , c.average_cluster_energy() ,str(c.nodelist) , str(c.TDMA_slots) ,str(c.CH),c.is_alive))
        print("****************************End of introduce network \n")


    def network_packet_summery(self):
        sumpout = 0
        sumpin = 0
        print("=================================Sent packet summery==============================")
        for n in self.nodes:
            print("node {0} sent {1} packes".format(n,len(n.outbox)))
            sumpout +=len(n.outbox)
        print("All packet numbers in outbox the  network is {0} ".format(sumpout))
        print("=================================Received packet summery==============================")
        for n in self.nodes:
            print("node {0} sent {1} packes".format(n,len(n.inbox)))
            sumpin +=len(n.inbox)
        print("All packet numbers in inbox the network is {0} \n".format(sumpin))
        print("{0} packets are lost on wireless sensor network".format(sumpout-sumpin))
        print("=================================")

    def CH_probablity(self):
        if(len(self.clusters)==0):
            print("there is no cluster to cal CH_prob")
        return float(len(self.clusters))/float(len(self.nodelist))

    def cluster_formation(self):
        
        
        for n in self.nodes:
            if n.id != 0:
                if n.is_alive == True:
                    if n.cluster not in self.clusters:
                        self.clusters.append(n.cluster)
        print(self.clusters)
        for c in self.clusters:
            mcluster = cluster.mycluster(c,self.env,self)
            for n in self.nodes:
                if n.cluster == c:
                    mcluster.add_node(n)

            print(mcluster.nodes)
            mcluster.Clusterhead_Selection()
