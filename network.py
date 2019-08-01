import simpy
import random
import node
import config
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
        controller = node.Node(0, self.env, (self.xsize)/2, (self.xsize)/2,node_type='B' )
        self.nodes.append(controller)
        controller.net = self
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



