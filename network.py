import simpy
import random
import node
import config
import math

"""
"""

class Net():
    def __init__(self,env,xsize=config.AREA_WIDTH,ysize=config.AREA_LENGTH):
        self.env = env
        self.action = env.process(self.run())
        self.clock = ["CSMA"]
        self.nodes = []
        self.xsize = xsize
        self.ysize = ysize

    
    def run(self):
        controller = node.Node(0, self.env, (self.xsize)/2, (self.xsize)/2,node_type='B' ,power_type=0)
        self.nodes.append(controller)
        controller.net = self
        print(" s n",self.nodes)
        counter = 0
        while True:
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
                print("inactive network",self.env.now)
                yield self.env.timeout(1)
            self.network_nodedsicovery()
            print(self.nodes)
            print("net discovery")

    def TDMA(self,duration):
        for i in range(duration):
            self.clock.clear()
            self.clock.append("TDMA")
            print("TDMA",self.env.now)
            yield self.env.timeout(1)

    def CSMA(self,duration):
        for i in range(duration):
            self.clock.clear()
            self.clock.append("CSMA")
            #print("CSMA",env.now)
            yield self.env.timeout(1)



    def random_net_generator(self,env,network,node_number):
        for i in range(node_number):
                mnode = node.Node(i+2,env ,2,random.randint(0,self.xsize),random.randint(0,self.ysize))
                mnode.net= self
                self.nodes.append(mnode)
        self.network_nodedsicovery()
        print("random")

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
                            print("{0} <=> {1} d= {2}".format(str(n.id) , str(n1.id) , math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2))))
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
            print("{0} is alive: {5} with energy : {1} with position {2} {3} ; CH is {4}".format(x.name , str(sum(x.energy)) ,str(x.x) , str(x.y) ,str(x.parent),x.is_alive))
        print("==============================Clusters===============================")
        # for c in self.clusters:
        #     print("{0} is alive: {5} with energy : {1} with nodes {2} ; TDMA: {3} ; CH is {4}".format(c.name , c.average_cluster_energy() ,str(c.nodelist) , str(c.TDMA_slots) ,str(c.CH),c.is_alive))
        print("****************************End of introduce network \n")
            