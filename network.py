import simpy
import random
import node
import config
import math
import RSSI
import cluster
import message
import gui
import alert
import config
import pandas as pd
import logger
"""
"""

class Net():
    def __init__(self,env,xsize=config.AREA_WIDTH,ysize=config.AREA_LENGTH):
        self.env = env
        self.action = env.process(self.run())
        self.clock = ["CSMA"]
        self.TDMA_slot = 0
        self.CSMA_slot =0
        self.nodes = []
        self.clusters = []
        self.clusterheads = []
        self.superframe_num = 0
        self.xsize = xsize
        self.ysize = ysize
        #add controller
        controller = node.Node(0, self.env,4, (self.xsize)/2, (self.ysize)/2,node_type='B' ,power_type=0)
        self.nodes.append(controller)
        controller.net = self
        self.alert = False
        self.logger = logger.logger()
        self.dfdead = pd.DataFrame(columns=['id','deadtime','remainedenergy'])

    def run(self):
        counter = 0
        initial = False
        initialalert = False
        is_solved = False

        while True:
            self.ClusterHead_finder()
            if (initial == False): # run once initialization
                try:
                    yield self.env.process(self.initialization(10))
                except simpy.Interrupt:
                    self.logger.log("Was interrupted.CSMA")
                    print('Was interrupted.CSMA')
                initial = True

            counter += 1 # count superframes
            self.superframe_num = counter
            self.logger.log('\n New Superframe is began CSMA at %d number %d\n' % (self.env.now ,counter))
            print('\n New Superframe is began CSMA at %d number %d\n' % (self.env.now ,counter))
            CSMA_duration = config.CSMA_duration

            if counter % config.Base_Sattion_Beaconning_period == 0:
                for n in self.nodes[0].neighbors:
                    message_sender = message.Message()
                    message_sender.broadcast(self.nodes[0],"Base Station boradcast on regular basis {0} at env:{1}".format(self.nodes[0].id ,self.env.now))

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

            self.neighbor_collision()

            #print('INACTIVE at %d\n' % env.now)
            inactive_duration = 14
            for i in range(inactive_duration):
                self.clock.clear()
                self.clock.append("INACTIVE")
                self.logger.log("at %d inactive network" %self.env.now)
                print("at %d inactive network" %self.env.now)
                yield self.env.timeout(1)
            # self.network_nodedsicovery()
            # print(self.nodes)
            # print("net discovery")

            if(initialalert == False):
                if self.env.now > config.ALERT_TIME:
                    self.alert = True
                    self.logger.log("Alert is created")
                    print("Alert is created")
                    try:
                        yield self.env.process(self.alert_creator())
                    except simpy.Interrupt:
                        print('Was interrupted.CSMA')
                    initialalert = True

            if(is_solved == False):
                if self.env.now > config.ALERT_END:
                    self.alert = False
                    self.logger.log("Alert is solved ")
                    print("Alert is solved ")
                    graphi = gui.graphic(self)
                    graphi.alert_sloved()
                    is_solved = True
            
            if self.alert == True: # if BS get alert
                if any("Alert" in s for s in self.nodes[0].inbox):
                    self.logger.log("Alertttttt is received by BS ".format( self.env.now))
                    print("Alertttttt is received by BS ".format( self.env.now))
                    


    def initialization(self,duration):
        self.logger.log("BS start to advertise + Superframe rules")
        print("BS start to advertise + Superframe rules")
        self.network_nodedsicovery()
        for n in self.clusterheads:
            self.nodes[0].neighbors.append(n)
        self.logger.log("neighbors of BS:{0}".format(self.nodes[0].neighbors))
        print("neighbors of BS: {0}".format(self.nodes[0].neighbors))
        for n in self.nodes[0].neighbors:
            # print(n,"is near bs")
            # n.distance.clear()
            n.distance.append(self.nodes[0])

        message_sender = message.Message()
        message_sender.broadcast(self.nodes[0],"BS boradcast + Superframe rules adv {0} at env:{1}".format(self.nodes[0].id ,self.env.now))
        self.logger.log('cluster formation\n')
        print('cluster formation\n')
        # self.cluster_formation()
        print("Inititial network %d nods at %d"%(len(self.nodes),self.env.now))
        yield self.env.timeout(duration)
        print("net is initials ends at {0} \n".format(self.env.now))
        

    def TDMA(self,duration):
        for i in range(duration):
            self.clock.clear()
            self.clock.append("TDMA")
            self.TDMA_slot = i+1
            self.logger.log("\n\nat {0} TDMA - slot {1}".format(self.env.now,(i+1)))
            print("\n\nat {0} TDMA - slot {1}".format(self.env.now,(i+1)))
            yield self.env.timeout(1)

    def CSMA(self,duration):
        for i in range(duration):
            self.clock.clear()
            self.clock.append("CSMA")
            self.CSMA_slot = i+1
            self.logger.log("\nat {0} CSMA - slot {1}".format(self.env.now,(i+1)))
            print("\nat {0} CSMA - slot {1}".format(self.env.now,(i+1)))
            yield self.env.timeout(1)


    def random_net_generator(self,env,network,node_number):
        print("Random network is generated with %d nodes\n"%node_number)
        for i in range(node_number):
                mnode = node.Node(i+1,env ,random.randint(1000,2000),random.randint(0,self.xsize),random.randint(0,self.ysize))
                self.add_node(mnode)
        self.network_nodedsicovery()
        #print("random")

    def add_node(self, node):
        #print (self.id) # debugging...
        self.nodes.append(node)
        node.net = self
        # self.network_nodedsicovery(distance = config.TX_RANGE,dprint=False)


    def network_nodedsicovery(self,distance = config.TX_RANGE):
        self.logger.log("++++++++++++++++++++ network Table Discovery Begins %d meters ++++++++++++++++++++++++++++"%config.TX_RANGE)
        print("++++++++++++++++++++ network Table Discovery Begins %d meters ++++++++++++++++++++++++++++"%config.TX_RANGE)
        for n in self.nodes:
            self.logger.log("Neighbors Table discovery for {0} is below and neighbors are {1}".format(str(n.id),n.neighbors))
            print("Neighbors Table discovery for {0} is below and neighbors are {1}".format(str(n.id),n.neighbors))
            for n1 in self.nodes:
                if(distance > math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2))):
                    if(n!=n1):
                        tempmessage = ("{0} your neighbor is {1} Distance= {2} RSSI= {3}".format(str(n.id) , str(n1.id) , round(math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2)),2),round(RSSI.RSSI_nodes(n,n1)),4))
                        message_sender = message.Message(tempmessage)
                        msg_len = message_sender.message_length()
                        message_sender.send_message(tempmessage,n,n1,TDMA=False)
                        self.logger.log("{0} <=> {1} Distance= {2} RSSI= {3}".format(str(n.id) , str(n1.id) , round(math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2)),2),round(RSSI.RSSI_nodes(n,n1)),4))
                        print("{0} <=> {1} Distance= {2} RSSI= {3}".format(str(n.id) , str(n1.id) , round(math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2)),2),round(RSSI.RSSI_nodes(n,n1)),4))
                        if n1 not in n.neighbors:
                            n.neighbors.append(n1)

        self.logger.log( "+++++++++++++++++++++ network Table Discovery Ends +++++++++++++++++++++++++++++++ \n")                   
        print("+++++++++++++++++++++ network Table Discovery Ends +++++++++++++++++++++++++++++++ \n")


    def distance(self, node ,node1):
        return math.sqrt(((node.x-node1.x)**2)+((node.y-node1.y)**2))


    def network_inboxes(self):
        self.logger.log("\nInboxes are shown: ")
        print("\nInboxes are shown: ")
        for n in self.nodes:
            self.logger.log("Inbox {0} has {1} \n".format(str(n.id) ,str(n.inbox)))
            print("Inbox {0} has {1} \n".format(str(n.id) ,str(n.inbox)))

    def network_outboxes(self):
        self.logger.log("\nOutboxes are shown: ")
        print("\nOutboxes are shown: ")
        for n in self.nodes:
            self.logger.log("Outbox {0} has {1} \n".format(str(n.id) ,str(n.outbox)))
            print("Outbox {0} has {1} \n".format(str(n.id) ,str(n.outbox)))

    def introduce_yourself(self):
        df = pd.DataFrame(columns=['id' , 'power', 'x' , 'y' , 'parent' ,'is_alive','TDMA','energy'])
        self.logger.log("****************************Begin of introduce network" )
        print("****************************Begin of introduce network" )
        # print("Network {0} with {1} node number with size {2} {3} and have {4} clusters".format(self.name,len(self.nodelist),self.xsize,self.ysize,len(self.clusterheads)))
        #print("New network is created : {0} with {1} node number ".format(self.name,self.nodelist.count))
        for x in self.nodes:
            if len(x.parent) == 0:
                self.logger.log("{0}  with energy : {1}  with position {2} {3} ; CH is {4} is alive: {5} with TDMA {6} {7}".format(x.id , x.power, str(x.x) , str(x.y) ,str(x.parent),x.is_alive,x.TDMA,next(reversed(x.energy))))
                print("{0}  with energy : {1}  with position {2} {3} ; CH is {4} is alive: {5} with TDMA {6} {7}".format(x.id , x.power, str(x.x) , str(x.y) ,str(x.parent),x.is_alive,x.TDMA,next(reversed(x.energy))))
                # print(x.energy)
                df = df. append(pd.Series([x.id , x.power, str(x.x) , str(x.y) ,str(x.parent),x.is_alive,x.TDMA,next(reversed(x.energy))], index=df.columns), ignore_index=True)
            if len(x.parent) != 0:
                self.logger.log("{0}  with energy : {1}  with position {2} {3} ; CH is {4} is alive: {5} with TDMA {6} {7}".format(x.id ,x.power, str(x.x) , str(x.y) ,str(next(reversed(x.parent))),x.is_alive,x.TDMA,next(reversed(x.energy))))
                print("{0}  with energy : {1}  with position {2} {3} ; CH is {4} is alive: {5} with TDMA {6} {7}".format(x.id ,x.power, str(x.x) , str(x.y) ,str(next(reversed(x.parent))),x.is_alive,x.TDMA,next(reversed(x.energy))))
                # print(x.energy)
                df = df. append(pd.Series([x.id , x.power, str(x.x) , str(x.y) ,str(x.parent),x.is_alive,x.TDMA,next(reversed(x.energy))], index=df.columns), ignore_index=True)
        self.logger.log("==============================Clusters===============================")
        print("==============================Clusters===============================")
        # for c in self.clusters:
        #     print("{0} is alive: {5} with energy : {1} with nodes {2} ; TDMA: {3} ; CH is {4}".format(c.name , c.average_cluster_energy() ,str(c.nodelist) , str(c.TDMA_slots) ,str(c.CH),c.is_alive))
        print("****************************End of introduce network \n")
        df.to_csv('report/introduce_yourself.csv')


    def network_packet_summery(self):
        sumpout = 0
        sumpin = 0
        df = pd.DataFrame(columns=['id','sent','received','lost'])
        self.logger.log("=================================Sent packet summery==============================")
        print("=================================Sent packet summery==============================")
        for n in self.nodes:
            self.logger.log("node {0} sent {1} packes".format(n,len(n.outbox)))
            print("node {0} sent {1} packes".format(n,len(n.outbox)))
            sumpout +=len(n.outbox)
        self.logger.log("All packet numbers in outbox the  network is {0} ".format(sumpout))
        print("All packet numbers in outbox the  network is {0} ".format(sumpout))
        self.logger.log("=================================Received packet summery==============================")
        print("=================================Received packet summery==============================")
        for n in self.nodes:
            self.logger.log("node {0} Received {1} packes".format(n,len(n.inbox)))
            print("node {0} Received {1} packes".format(n,len(n.inbox)))
            sumpin +=len(n.inbox)
            df = df.append(pd.Series([n,len(n.outbox),len(n.inbox),len(n.outbox)-len(n.inbox)], index=df.columns), ignore_index=True)
        self.logger.log("All packet numbers in inbox the network is {0} \n".format(sumpin))
        print("All packet numbers in inbox the network is {0} \n".format(sumpin))
        self.logger.log("{0} packets are lost on wireless sensor network".format(sumpout-sumpin))
        print("{0} packets are lost on wireless sensor network".format(sumpout-sumpin))
        print("=================================")
        df.to_csv('report/packet.csv')
                        

    def savedeadnodes(self,i,energy,now):
        self.dfdead.append(pd.Series([i,energy,now], index=self.dfdead.columns), ignore_index=True)
        self.dfdead.to_csv('report/deadnodes.csv')

    def CH_probablity(self):
        if(len(self.clusters)==0):
            print("there is no cluster to cal CH_prob")
        return float(len(self.clusters))/float(len(self.nodes))

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

    def add_cluster(self, cluster):
        self.clusters.append(cluster)
        cluster.network = self
        #print ("{0} network has cluster id {1}".format(self.name,cluster.id))

    def remove_cluster(self, cluster):
        self.clusters.remove(cluster)

    def ClusterHead_finder(self):
        self.clusterheads.clear()
        for n in self.nodes:
            if(n.is_alive==True):
                if (n.is_CH == True):
    
                    self.clusterheads.append(n)
                    self.clusterheads =  list(dict.fromkeys(self.clusterheads)) # remove duplicates
        # print("clusterheads are {0} in network  \n".format(self.clusterheads))
    
    def neighbor_collision(self): # check if 2 nodes neighbor have same TDMA
        for n1 in self.nodes:
            for n2 in self.nodes:
                if n1.id != 0 :
                    if n2.id !=0:
                        if (n1.is_CH == False) and (n2.is_CH == False):
                            if n1 in n2.neighbors:
                                if n1.TDMA == n2.TDMA:
                                    self.logger.log("{0} {1} {2} {3} {4} ".format(n1,n1.TDMA,"collison TDMA",n2,n2.TDMA))
                                    print("{0} {1} {2} {3} {4} ".format(n1,n1.TDMA,"collison TDMA",n2,n2.TDMA))
                                    n2.TDMA = len(n2.clus.nodes) + 1


    def alert_creator(self): # create alert in the network
        alert1 = alert.Alert(self.env,config.alertx,config.alerty,self)
        graphi = gui.graphic(self)
        graphi.alert()

        yield self.env.timeout(1)

