import simpy
import random
import node
import config
import math
import RSSI
import cluster
import message
import gui
#import alert
import config
import pandas as pd
import logger
from superframe import Superframe
import pickle
from interference import Interference
import time
#import mac
"""
"""

class Net():
    def __init__(self,env ,xsize = config.AREA_WIDTH, ysize = config.AREA_LENGTH):
        self.env = env
        # superframe
        self.clock = ["CSMA"]
        self.superframe = Superframe()
        self.TDMA_slot = 0
        self.CSMA_slot = 0
        self.inactive_duration = 0
         # we can set here
        self.nodes = []
        self.clusters = []
        self.clusterheads = []
        self.superframe_num = 0

        #add controller
        # controller = node.Node(0, self.env, 4, (config.xsize)/2, (config.ysize)/2, node_type='B' ,power_type=0)
        # self.nodes.append(controller)
        # controller.net = self
        self.logger = logger.logger()
        #self.dfdead = pd.DataFrame(columns=['id','deadtime','remainedenergy'])
        #self.mac = mac.Mac(self.env,self)

        self.interfrerence = Interference(self.env,self)
        self.action = env.process(self.run())
        self.channel_free = True

    def run(self):
        counter = 0
        initial = False
        is_solved = False


        while True:
            #self.clock = self.mac.clock
            # if(self.env.now % 700 == 0):
                #if(config.guienabled):

                #   graph = gui.graphic(self)
                    #graph.draw()  
                
            if (initial == False): # run once initialization
                try:
                    yield self.env.process(self.initialization(10))
                except simpy.Interrupt:
                    self.logger.log("Was interrupted.CSMA")
                    if config.printenabled:
                        print('Was interrupted.CSMA')
                initial = True

            counter += 1 # count superframes
            self.superframe_num = counter
            self.logger.log('\n New Superframe is began CSMA at %d number %d\n' % (self.env.now ,counter))
            if config.printenabled:

                print('\n New Superframe is began CSMA at %d number %d\n' % (self.env.now ,counter))
            CSMA_duration = self.superframe.CSMA_slot

            if counter % config.Base_Sattion_Beaconning_period == 0: #beaconing the BS to sync the time and check the routs
                if config.printenabled:
                    print("Base Station beacon on regular basis {0} at env:{1} to sync the time and check the routs".format(config.Base_Sattion_Beaconning_period ,self.env.now))

                for n in self.nodes[0].neighbors:
                    message_sender = message.Message()
                    message_sender.broadcast(self.nodes[0],"Base Station beacon on regular basis {0} at env:{1} to sync the time and check the routs".format(self.nodes[0].id ,self.env.now),n.neighbors)

            try:
                yield self.env.process(self.CSMA(CSMA_duration))
            except simpy.Interrupt:
                if config.printenabled:
                    print('Was interrupted.CSMA')

            #print('TDMA at %d\n' % env.now)
            TDMA_duration = self.superframe.TDMA_slot

            try:
                yield self.env.process(self.TDMA(TDMA_duration))
            except simpy.Interrupt:
                if config.printenabled:
                    print('Was interrupted.TDMA')

            self.neighbor_collision()


            try:
                yield self.env.process(self.INACTIVE(self.superframe.Inactive_slot))
            except simpy.Interrupt:
                if config.printenabled:
                    print('Was interrupted.INACTIVE')
            # self.ieee802154_nodedsicovery()
            # print(self.nodes)
            # print("net discovery")

            self.interfrerence

                

    def initialization(self,duration):
        self.logger.log("initialization BS start to advertise + Superframe rules")
        if config.printenabled:
            print("initialization BS start to advertise + Superframe rules")
        self.ieee802154_nodedsicovery()
        if (len(self.clusterheads) != 0):
            for n in self.clusterheads:
                self.nodes[0].neighbors.append(n)
            self.logger.log("neighbors of BS:{0}".format(self.nodes[0].neighbors))
            if config.printenabled:
                print("neighbors of BS: {0}".format(self.nodes[0].neighbors))
        else:
            if config.printenabled:
                print("Clusterheads' list is empty")
        self.introduce_yourself()
        # for n in self.nodes[0].neighbors:
        #     print(n,"is near bs")
        #     # n.distance.clear()
        #     n.distance.append(self.nodes[0])

        message_sender = message.Message(header='superframe',data=self.superframe)
        message_sender.broadcast(self.nodes[0],nodelist=self.nodes)

        for n in self.nodes:
            message_sender.send_message("BS boradcast + Superframe rules adv " + str(n.id),self.nodes[0],n)
        #message_sender.broadcast(self.nodes[0],"BS boradcast + Superframe rules adv {0} at env:{1}".format(self.nodes[0].id ,self.env.now))
        #self.logger.log('cluster formation\n')
        if config.printenabled:
            print("Inititial ieee802154 %d nods at %d"%(len(self.nodes),self.env.now))
        yield self.env.timeout(duration)
        if config.printenabled:
            print("net is initials ends at {0} \n".format(self.env.now))
        
    #clock
    def TDMA(self,duration):
        for i in range(duration+1):
            self.clock.clear()
            self.clock.append("TDMA")
            self.TDMA_slot = i+1
            self.logger.log("\n\nat {0} TDMA - slot {1}".format(self.env.now,(i)))
            if config.printenabled:
                print("\n\nat {0} TDMA - slot {1}".format(self.env.now,(i)))

            yield self.env.timeout(1)

    def CSMA(self,duration):
        for i in range(duration):
            self.channel_free = True
            self.clock.clear()
            self.clock.append("CSMA")
            self.CSMA_slot = i+1
            self.logger.log("\nat {0} CSMA - slot {1}".format(self.env.now,(i+1)))
            if config.CSMA_duration < len(self.clusterheads): #penalty for not enough slot for SCMA
                for node in self.clusterheads:
                    #print(self.clusterheads)
                    #print(random.getrandbits(1))
                    if random.randint(1, len(self.clusterheads)) < ( len(self.clusterheads)-config.CSMA_duration ):
                        node.power.decrease_tx_energy(10000)
                        node.energy.append(node.power.energy)

            if config.printenabled:
                print("\nat {0} CSMA - slot {1}".format(self.env.now,(i+1)))

            yield self.env.timeout(1)
    
    def INACTIVE(self,duration):

        for i in range(duration):
            self.clock.clear()
            self.clock.append("INACTIVE")
            self.CSMA_slot = i+1 
            self.logger.log("at %d inactive ieee802154" %self.env.now)
            if config.printenabled:
                print("at %d inactive ieee802154" %self.env.now)

            yield self.env.timeout(1)


    def random_net_generator(self,env,ieee802154,node_number):
        if config.printenabled:
            print("Random ieee802154 is generated with %d nodes\n"%node_number)
        for i in range(node_number):
                mnode = node.Node(i+1,env ,random.randint(1000,2000),random.randint(0,self.xsize),random.randint(0,self.ysize))
                self.add_node(mnode)
        self.ieee802154_nodedsicovery()
        #print("random")

    def add_node(self, node):
        #print (self.id) # debugging...
        self.nodes.append(node)
        node.net = self
        # self.ieee802154_nodedsicovery(distance = config.TX_RANGE,dprint=False)


    def ieee802154_nodedsicovery(self,distance = config.TX_RANGE):
        self.logger.log("\n++++++++++++++++++++ ieee802154 Table Discovery Begins %d meters ++++++++++++++++++++++++++++"%config.TX_RANGE)
        if config.printenabled:
            print("++++++++++++++++++++ ieee802154 Table Discovery Begins %d meters ++++++++++++++++++++++++++++"%config.TX_RANGE)
        for n in self.nodes:
            self.logger.log("Neighbors Table discovery for {0} is below and neighbors are {1}".format(str(n.id),n.neighbors))
            #print("Neighbors Table discovery for {0} is below and neighbors are {1}".format(str(n.id),n.neighbors))
            for n1 in self.nodes:
                if(distance > math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2))):
                    if(n!=n1):
                        tempmessage = ("a{0} your neighbor is {1} Distance= {2} RSSI= {3}".format(str(n.id) , str(n1.id) , round(math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2)),2),round(RSSI.RSSI_nodes(n,n1)),4))
                        message_sender = message.Message(tempmessage)
                        msg_len = message_sender.message_length()
                        message_sender.send_message(tempmessage,n,n1,TDMA=False)
                        self.logger.log("{0} <=> {1} Distance= {2} RSSI= {3}".format(str(n.id) , str(n1.id) , round(math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2)),2),round(RSSI.RSSI_nodes(n,n1)),4))
                        #print("{0} <=> {1} Distance= {2} RSSI= {3}".format(str(n.id) , str(n1.id) , round(math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2)),2),round(RSSI.RSSI_nodes(n,n1)),4))
                        if n1 not in n.neighbors:
                            n.neighbors.append(n1)

        self.logger.log( "+++++++++++++++++++++ ieee802154 Table Discovery Ends +++++++++++++++++++++++++++++++ \n")                   
        if config.printenabled:
            print("+++++++++++++++++++++ ieee802154 Table Discovery Ends +++++++++++++++++++++++++++++++ \n")


    def distance(self, node ,node1):
        return math.sqrt(((node.x-node1.x)**2)+((node.y-node1.y)**2))


    def ieee802154_inboxes(self):
        self.logger.log("\nInboxes are shown: ")
        if config.printenabled:
            print("\nInboxes are shown: ")
        for n in self.nodes:
            self.logger.log("Inbox {0} has {1} \n".format(str(n.id) ,str(n.inbox)))
            if config.printenabled:
                print("Inbox {0} has {1} \n".format(str(n.id) ,str(n.inbox)))

    def ieee802154_outboxes(self):
        self.logger.log("\nOutboxes are shown: ")
        if config.printenabled:
            print("\nOutboxes are shown: ")
        for n in self.nodes:
            self.logger.log("Outbox {0} has {1} \n".format(str(n.id) ,str(n.outbox)))
            if config.printenabled:
                print("Outbox {0} has {1} \n".format(str(n.id) ,str(n.outbox)))

    def introduce_yourself(self):
        dfi = pd.DataFrame(columns=['id' , 'power', 'x' , 'y' , 'parent' ,'is_alive','TDMA','energy'])
        self.logger.log("****************************Begin of introduce ieee802154" )
        if config.printenabled:
            print("****************************Begin of introduce ieee802154" )

        for x in self.nodes:
            #print(x.id," is_CH ",x.is_CH,x.parent)
            if len(x.parent) == 0:
                self.logger.log("{0}  with energy : {1}  with position {2} {3} ; CH is {8} {4} is alive: {5} with TDMA {6} {7}".format(x.id , x.power, str(x.x) , str(x.y) ,str(x.parent),x.is_alive,x.TDMA,next(reversed(x.energy)),x.is_CH))
                if config.printenabled:
                    print("{0}  with energy : {1}  with position {2} {3} ; CH is {8} {4} is alive: {5} with TDMA {6} {7}".format(x.id , x.power, str(x.x) , str(x.y) ,str(x.parent),x.is_alive,x.TDMA,next(reversed(x.energy)),x.is_CH))
                # print(x.energy)
                dfi = dfi. append(pd.Series([x.id , x.power, str(x.x) , str(x.y) ,str(x.parent),x.is_alive,x.TDMA,next(reversed(x.energy))], index=dfi.columns), ignore_index=True)
            if len(x.parent) != 0:
                self.logger.log("{0}  with energy : {1}  with position {2} {3} ; CH is {9} {4} is alive: {5} with TDMA {6} {7} sensor t: {8}".format(x.id ,x.power, str(x.x) , str(x.y) ,str(next(reversed(x.parent))),x.is_alive,x.TDMA,next(reversed(x.energy)),x.sensor,x.is_CH))
                if config.printenabled:
                    print("{0}  with energy : {1}  with position {2} {3} ; CH is {9} {4} is alive: {5} with TDMA {6} {7} sensor t: {8}".format(x.id ,x.power, str(x.x) , str(x.y) ,str(next(reversed(x.parent))),x.is_alive,x.TDMA,next(reversed(x.energy)),x.sensor,x.is_CH))
                # print(x.energy)
                dfi = dfi. append(pd.Series([x.id , x.power, str(x.x) , str(x.y) ,str(x.parent),x.is_alive,x.TDMA,next(reversed(x.energy))], index=dfi.columns), ignore_index=True)
        #self.logger.log("==============================Clusters===============================")
        #print("==============================Clusters===============================")
        # for c in self.clusters:
        #     print("{0} is alive: {5} with energy : {1} with nodes {2} ; TDMA: {3} ; CH is {4}".format(c.name , c.average_cluster_energy() ,str(c.nodelist) , str(c.TDMA_slots) ,str(c.CH),c.is_alive))
        if config.printenabled:
            print("****************************End of introduce ieee802154 \n")
        if(config.excelsave):
            dfi.to_csv('report/introduce_yourself.csv')
        #pickle.dump(self.nodes, file = open("report/nodes.pickle", "wb"))



    def ieee802154_packet_summery(self):
        sumpout = 0
        sumpin = 0
        dfp = pd.DataFrame(columns=['id','sent','received','lost'])
        self.logger.log("================================= packet summery==============================")
        if config.printenabled:
            print("================================= packet summery==============================")
        for n in self.nodes:
            if (n.id !=0):
                self.logger.log("node {0} Sent {1} packes and Received {2} packes".format(n,len(n.outbox),len(n.inbox)))
                if config.printenabled:
                    print("node {0} Sent {1} packes and Received {2} packes Lost : {3}".format(n,len(n.outbox),len(n.inbox),len(n.outbox)-len(n.inbox)))
                dfp = dfp.append(pd.Series([n,len(n.outbox),len(n.inbox),len(n.outbox)-len(n.inbox)], index=dfp.columns), ignore_index=True)
                sumpout += len(n.outbox)
                sumpin += len(n.inbox)
        self.logger.log("{0} packets are lost on wireless sensor ieee802154".format(sumpout-sumpin))
        if config.printenabled:
            print("{0} packets are lost on wireless sensor ieee802154 {1} {2}".format(sumpout-sumpin,sumpout,sumpin))
            print("=================================")
        if(config.excelsave):
            dfp.to_csv('report/packet.csv')
            if config.printenabled:
                print(dfp.sum(axis = 0, skipna = True))
                            

    # def savedeadnodes(self,i,energy,now):
    #     self.dfdead.append(pd.Series([i,energy,now], index=self.dfdead.columns), ignore_index=True)
    #     self.dfdead.to_csv('report/deadnodes.csv')


    def add_cluster(self, cluster):
        self.clusters.append(cluster)
        cluster.ieee802154 = self
        #print ("{0} ieee802154 has cluster id {1}".format(self.name,cluster.id))

    def remove_cluster(self, cluster):
        self.clusters.remove(cluster)

    
    def neighbor_collision(self): # check if 2 nodes neighbor have same TDMA
        for n1 in self.nodes:
            for n2 in self.nodes:
                if n1.id != 0 :
                    if n2.id !=0:
                        if (n1.is_CH == False) and (n2.is_CH == False):
                            if n1 in n2.neighbors:
                                if n1.TDMA == n2.TDMA:
                                    self.logger.log("{0} {1} {2} {3} {4} ".format(n1,n1.TDMA,"collison TDMA",n2,n2.TDMA))
                                    if config.printenabled:
                                        print("{0} {1} {2} {3} {4} ".format(n1,n1.TDMA,"collison TDMA",n2,n2.TDMA))
                                    if n2.TDMA+1 < 7:
                                        n2.TDMA = n2.TDMA+1
                                    else:
                                        if config.printenabled:

                                            print("neighbor collision")
                                    #n2.TDMA = len(n2.clus.nodes) + 1



    def ieee802154_optimize(self):
        # energy
        energy = 0
        for n in self.nodes:
            if(next(reversed(n.energy)) > 0):
                energy = energy + next(reversed(n.energy))
                #print(next(reversed(n.energy)))
        self.logger.log("avrage ieee802154 energy {0}".format(energy))
        if config.printenabled:
            print("{0} average ieee802154 energy {1}".format(time.ctime,energy))

        # duration
        duration = config.TDMA_duration + config.Duration + config.Inactive_duration
        if config.printenabled:
            print("duration ={0} superframe {1} {2} and t1:{3} t2:{4} t3:{5}".format(config.Duration,config.Multiframe_size,config.Multiframe_state,config.TDMA_duration,config.CSMA_duration,config.Inactive_duration))
            print("Max run is {} and number of superframe {} ".format(config.MAX_RUNTIME,self.superframe_num))
            print("P_TX is {} and P_RX is {}".format(config.P_TX,config.P_RX))
        # packet lost
        sumpout = 0
        sumpin = 0
        for n in self.nodes:
             if (n.id !=0):
                sumpout +=len(n.outbox)
                sumpin +=len(n.inbox)

        lost = sumpout-sumpin
        #if config.printenabled:
                #print("{0} packets are lost on wireless sensor ieee802154".format(lost))
        # first node
        t = []
        for n in self.nodes:
            t.append(n.deadtime)
        #if config.printenabled:
            #print("first node {0} in total run = {1}".format(min(t),config.MAX_RUNTIME))
        #
        return [energy,duration,lost,min(t)]