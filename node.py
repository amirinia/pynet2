import simpy
import network
import random 
import config
import message
from energymodel import EnergyModel
import sensor

class Node():
    def __init__(self,id,env,energy=(config.INITIAL_ENERGY-random.randint(0,2000)),x=random.randint(0,200),y=random.randint(0,200),node_type=None, power_type=1, mobile_type=0, network=network ):
        self.env = env
        self.id = id
        self.action = env.process(self.run())
        self.net = network
        self.is_alive = True
        self.energy = [2]
        print("node is created ")
        self.is_CH = False
        self.x = x
        self.y = y
        self.neighbors = []
        self.inbox = []
        self.parent = []
        self.power = EnergyModel(power_type=power_type)
        self.sensor = sensor.sensor(self.id,str(self.id)+"sensor")

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str("node"+str(self.id))

    def run(self):
        print("node is runing")
        while True:
            if(self.is_alive == True):
                        if (sum(self.energy) <= config.DEAD_NODE_THRESHOLD ):
                            print("^^^^^^^^^^node {0} is dead ith energy {1} at env:{2}^^^^^^^^^^^ \n".format(self.id,self.energy,self.env.now))
                            if(self.is_CH == True):
                                print("ch is dead we need find another one")
                                self.is_CH == False
                            self.is_alive = False

            if self.net.clock[0]=="TDMA":
                print("node%d is working TDMA %d "%(self.id,self.env.now))
                yield self.env.timeout(1)
                try:
                    if(self.is_alive == True):
                        yield self.env.process(self.node_beaconing(self.env))
                except simpy.Interrupt:
                    print("inter")

            elif self.net.clock[0]=="CSMA":
                if(self.is_CH == True):
                    print("CH talks in CSMA %d  %d "%(self.env.now,self.is_CH))
                yield self.env.timeout(1)

            else:
                #print("Inactive",self.env.now)
                yield self.env.timeout(1)


    def node_beaconing(self,env):
        message_sender = message.Message()
        if(self.is_alive == True): #if node is alive
            if len(self.parent) == 0: # if node has no parent ,beacons
                if(self.is_CH == False):
                    yield self.env.timeout(1)
                    print("at {0} beacon adv is sent by {1} is alive {2}, since it has no CH with energy {3}".format(env.now,self.id,self.is_alive,self.energy))
                    msg_len = message_sender.message_length()
                    self.power.decrease_tx_energy(msg_len)
                    self.energy.append(self.power.energy)


                    for n in self.neighbors:
                        message_sender.broadcast(n,"beacon adv {0} at env:{1}".format(n.id ,env.now))

            if (len(self.parent) != 0): # if node has parent send data to parent
                if((env.now % self.TDMA )==0):
                    yield self.env.timeout(self.TDMA_slot_number)
                    if(self.parent[0].is_alive == True):
                        print("at env:{3} light: {0} temperature: {1} from node {2} TDMA-based to {4} with pos {5} {6}".format(self.sensor.light_sensor(),self.sensor.temperature_sensor(),self.id,env.now,self.parent[0],self.x,self.y))
                        message_sender.send_message("at env:{3} light: {0} temperature: {1} from node {2} to {4}".format(self.sensor.light_sensor(),self.sensor.temperature_sensor(),self.id,env.now,self.parent[0]),self,self.parent[0])
                    msg_len = message_sender.message_length()
                    self.power.decrease_tx_energy(msg_len)
                    self.energy.append(self.power.energy)
                    yield self.env.timeout(1)
            if (self.is_CH == True): # if node is cluster head

                self.power.decrease_energy(discharging_time=100)  # idle discharge

                yield self.env.timeout(config.AGGREGATE_TIME+self.TDMA)
                self.node_send_message(self.aggregate,0)
                self.aggregate.clear()
                print("CH {0} aggregate sent to BS on env:{1}================================+++++++++++++++++++++++++++++++++++++++++++++++ \n".format(self.id,env.now))
                