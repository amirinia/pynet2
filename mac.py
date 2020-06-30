import simpy
import random
import node
import config
import math
import RSSI
import cluster
import message
import config
import network
import logger
import pandas as pd
from superframe import Superframe
from interference import Interference
"""
"""

class Mac():
    def __init__(self,env ,network=network):
        self.env = env
        # superframe
        self.clock = ["CSMA"]
        self.superframe = Superframe()
        self.TDMA_slot = 0
        self.CSMA_slot = 0
        self.inactive_duration = 0
        self.superframe_num = 0
        self.net = network
        self.logger = logger.logger()

        #self.interfrerence = Interference(self.env,self)
        self.action = env.process(self.run())


    def run(self):
        counter = 0
        initial = False

        while True:           
            print("mac ", self.TDMA_slot,self.CSMA_slot,self.inactive_duration)   
            if (initial == False): # run once initialization
                try:
                    yield self.env.process(self.initialization(10))
                except simpy.Interrupt:
                    self.logger.log("Was interrupted.CSMA")
                    print('Was interrupted.CSMA')
                initial = True

            counter += 1 # count superframes
            self.superframe_num = counter
            self.logger.log('\n MAC New Superframe is began CSMA at %d number %d\n' % (self.env.now ,counter))
            print('\n MAC New Superframe is began CSMA at %d number %d\n' % (self.env.now ,counter))
            CSMA_duration = self.superframe.CSMA_slot
            yield self.env.timeout(32)


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



            #print('INACTIVE at %d\n' % env.now)
            inactive_duration = self.superframe.Inactive_slot
            try:
                yield self.env.process(self.INACTIVE(inactive_duration))
            except simpy.Interrupt:
                print('Was interrupted.INACTIVE')


            #self.interfrerence


    def initialization(self,duration):
        self.logger.log("initialization MAC")
        print("initialization MAC")

        yield self.env.timeout(duration)
        print("MAC is initials ends at {0} \n".format(self.env.now))
        

    def TDMA(self,duration):
        for i in range(duration+1):
            self.clock.clear()
            self.clock.append("TDMA")
            self.TDMA_slot = i+1
            self.logger.log("\n\nat {0} TDMA - slot {1}".format(self.env.now,(i)))
            print("\n\n mac at {0} TDMA - slot {1}".format(self.env.now,(i)))

            yield self.env.timeout(1)

    def CSMA(self,duration):
        for i in range(duration):
            self.clock.clear()
            self.clock.append("CSMA")
            self.CSMA_slot = i+1
            self.logger.log("\nat {0} CSMA - slot {1}".format(self.env.now,(i+1)))
            print("\n mac at {0} CSMA - slot {1}".format(self.env.now,(i+1)))

            yield self.env.timeout(1)

    def INACTIVE(self,duration):
        for i in range(duration):
            self.clock.clear()
            self.clock.append("INACTIVE")
            self.CSMA_slot = i+1
            self.logger.log("at %d inactive network" %self.env.now)
            print("mac at %d inactive network" %self.env.now)

            yield self.env.timeout(1)