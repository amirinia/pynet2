import simpy
import random
import node
import config
import math
import RSSI
import cluster
import message
import config
import pandas as pd
from superframe import Superframe
from interference import Interference
"""
"""

class Mac():
    def __init__(self,env ,superframe = Superframe()):
        self.env = env
        # superframe
        self.clock = ["CSMA"]
        self.superframe = Superframe()
        self.TDMA_slot = superframe.TDMA_slot
        self.CSMA_slot = superframe.CSMA_slot
        self.inactive_duration = superframe.Inactive_slot
        self.superframe_num = 0
        self.interfrerence = Interference(self.env,self)
        self.action = env.process(self.run())


    def run(self):
        counter = 0
        initial = False

        while True:              
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
            CSMA_duration = self.superframe.CSMA_slot

            if counter % config.Base_Sattion_Beaconning_period == 0:
                for n in self.nodes[0].neighbors:
                    message_sender = message.Message()
                    message_sender.broadcast(self.nodes[0],"Base Station boradcast on regular basis {0} at env:{1}".format(self.nodes[0].id ,self.env.now),n.neighbors)

            try:
                yield self.env.process(self.CSMA(CSMA_duration))
            except simpy.Interrupt:
                print('Was interrupted.CSMA')

            #print('TDMA at %d\n' % env.now)
            TDMA_duration = self.superframe.TDMA_slot

            try:
                yield self.env.process(self.TDMA(TDMA_duration))
            except simpy.Interrupt:
                print('Was interrupted.TDMA')

            self.neighbor_collision()

            #print('INACTIVE at %d\n' % env.now)
            inactive_duration = self.Inactive_duration
            try:
                yield self.env.process(self.INACTIVE(inactive_duration))
            except simpy.Interrupt:
                print('Was interrupted.INACTIVE')
            # self.network_nodedsicovery()
            # print(self.nodes)
            # print("net discovery")

            self.interfrerence


    def initialization(self,duration):
        self.logger.log("initialization BS start to advertise + Superframe rules")
        print("initialization BS start to advertise + Superframe rules")
        self.network_nodedsicovery()
        if (len(self.clusterheads) != 0):
            for n in self.clusterheads:
                self.nodes[0].neighbors.append(n)
            self.logger.log("neighbors of BS:{0}".format(self.nodes[0].neighbors))
            print("neighbors of BS: {0}".format(self.nodes[0].neighbors))
        else:
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

        print("Inititial network %d nods at %d"%(len(self.nodes),self.env.now))
        yield self.env.timeout(duration)
        print("net is initials ends at {0} \n".format(self.env.now))
        

    def TDMA(self,duration):
        for i in range(duration+1):
            self.clock.clear()
            self.clock.append("TDMA")
            self.TDMA_slot = i+1
            self.logger.log("\n\nat {0} TDMA - slot {1}".format(self.env.now,(i)))
            print("\n\nat {0} TDMA - slot {1}".format(self.env.now,(i)))

            yield self.env.timeout(1)

    def CSMA(self,duration):
        for i in range(duration):
            self.clock.clear()
            self.clock.append("CSMA")
            self.CSMA_slot = i+1
            self.logger.log("\nat {0} CSMA - slot {1}".format(self.env.now,(i+1)))
            print("\nat {0} CSMA - slot {1}".format(self.env.now,(i+1)))

            yield self.env.timeout(1)

    def INACTIVE(self,duration):
        for i in range(duration):
            self.clock.clear()
            self.clock.append("INACTIVE")
            self.CSMA_slot = i+1
            self.logger.log("at %d inactive network" %self.env.now)
            print("at %d inactive network" %self.env.now)

            yield self.env.timeout(1)