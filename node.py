import simpy
import network
import random 
import config
import message
from energymodel import EnergyModel
import sensor
import time

class Node():
    def __init__(self,id,env,energy=(config.INITIAL_ENERGY-random.randint(0,2000)),x=random.randint(0,config.AREA_WIDTH),y=random.randint(0,config.AREA_LENGTH),node_type=None, power_type=1, mobile_type=0, network=network ):
        self.env = env
        self.id = id
        self.action = env.process(self.run())
        self.net = network
        self.is_alive = True
        self.energy = [2]
        #print("node is created ")
        self.is_CH = False
        self.x = x
        self.y = y
        self.neighbors = []
        self.inbox = []
        self.outbox = []
        self.parent = []
        self.cluster = []
        self.TDMA = 0
        self.power = EnergyModel(power_type = power_type)
        self.sensor = sensor.sensor(self.id,str(self.id) + "sensor")

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str("node"+str(self.id))

    def run(self):
        # print("node is runing",self.id)
        if self.id != 0:
            while True:
                if(self.is_alive == True):
                    #print(next(reversed(self.energy)))
                    if (next(reversed(self.energy)) <= config.DEAD_NODE_THRESHOLD ):
                        print("^^^^^^^^^^node {0} is dead ith energy {1} at env:{2}^^^^^^^^^^^ \n".format(self.id,next(reversed(self.energy)),self.env.now))
                        if(self.is_CH == True):
                            print("ch is dead we need find another one")
                            self.is_CH == False
                        self.is_alive = False

                if self.net.clock[0]=="TDMA":
                    # print("at {0} node {1} is working on TDMA {2} cluster {3} ".format(self.env.now,self.id,self.TDMA,self.cluster))
                    yield self.env.timeout(1)
                    try:
                        if(self.is_alive == True):
                            yield self.env.process(self.node_beaconing(self.env))
                    except simpy.Interrupt:
                        print("inter")

                elif self.net.clock[0]=="CSMA":
                    if(self.is_CH == True):
                        print("at %d CH talks in CSMA   %d "%(self.env.now,self.is_CH))
                    yield self.env.timeout(1)

                else:
                    #print("Inactive",self.env.now) # inactive time
                    yield self.env.timeout(1)


    def node_beaconing(self,env):
        message_sender = message.Message()
        if(self.is_alive == True): #if node is alive
            if len(self.parent) == 0: # if node has no parent ,beacons
                if(self.is_CH == False):
                    yield self.env.timeout(1)
                    print("at {0} beacon adv is sent by {1} is alive {2}, since it has no CH with energy {3}".format(env.now,self.id,self.is_alive,self.power))
                    msg_len = message_sender.message_length()
                    self.power.decrease_tx_energy(msg_len)
                    self.energy.append(self.power.energy)

                    for n in self.neighbors:
                        message_sender.broadcast(n,"beacon adv {0} at env:{1}".format(n.id ,env.now))

            if (len(self.parent) != 0): # if node has parent send data to parent
                if self.TDMA != 0:
                    if(((self.env.now % config.TDMA_duration)==self.TDMA )):
                        # print(self.id,"I have parent",self.TDMA,"at",self.env.now,"cluster",self.cluster)
                        print("at env:{3} light: {0} temperature: {1} from node {2} TDMA-based {4} to {5} with pos {6} {7}".format(self.sensor.light_sensor(),self.sensor.temperature_sensor(),self.id,env.now,self.TDMA,self.cluster,self.x,self.y))

                        # yield self.env.timeout(config.CSMA_duration+config.Inactive_duration)
                        # if(self.parent[-1].is_alive == True):
                        # message_sender.send_message("at env:{3} light: {0} temperature: {1} from node {2} to {4}".format(self.sensor.light_sensor(),self.sensor.temperature_sensor(),self.id,env.now,self.parent[0]),self,self.parent[0])
                    msg_len = message_sender.message_length()
                    self.power.decrease_tx_energy(msg_len)
                    self.energy.append(self.power.energy)
                    yield self.env.timeout(1)
            
            if (self.is_CH == True): # if node is cluster head
                self.power.decrease_energy(discharging_time = 100)  # idle discharge
                yield self.env.timeout(config.AGGREGATE_TIME + self.TDMA)
                self.node_send_message(self.aggregate,0)
                self.aggregate.clear()
                print("CH {0} aggregate sent to BS on env:{1}================================+++++++++++++++++++++++++++++++++++++++++++++++ \n".format(self.id,env.now))


    def node_send_message(self, str_message , node):
        #print("message {0} is sent^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ from {1} to {2}".format(str_message,self.id,node))
        self.outbox.append(str_message)


    def node_receive_message(self, str_message ,sender_node):
        self.inbox.append(str_message)
        if(self.is_CH == True): # if node is CH then aggregate
            self.aggregate.append(str_message)
        #self.send_ACK(sender_node)
        #print(self.name + " node_receive_message&&&&&&&&&&&&&&*************** " + str_message + " from "+ sender_node.name )
        if( "is cluster Head" in str_message ):
            self.change_TDMA(sender_node.TDMA)
            self.parent_setter(sender_node)
            if(self.is_CH == True):
                self.change_CulsterHead()

        
        if( "BS" in str_message):
            print("temp",self.name)
            time.sleep(2)
            for n in self.neighbors:
                print(n,self)
                if any("BS" in s for s in n.inbox):
                    print("temp inbox",self.name)
                    message1 = message.MyMessage()
                    message1.broadcast(n,"BS+{0}".format(self))
                    print(n.outbox ,n.name)
                    print(n.inbox ,n.name)
    
    def send_ACK(self,destination_node):
        message1 = message.MyMessage()
        #message1.send_message("ack",cls,destination_node)

    def parent_setter(self,ch):
        self.parent.append(ch)
        #print(ch, "is head")

    def change_to_clusterhead(self):
        message_sender = message.Message()
        self.is_CH == True

    def add_nodes(self,list):
        self.neighbors.append(list)