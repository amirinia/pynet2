import simpy
import network
import random 
import config
import message
from energymodel import EnergyModel
import sensor
import time
import gui
import cluster

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
        self.clus = cluster
        self.cluster = []
        self.TDMA = 0
        self.power = EnergyModel(power_type = power_type)
        self.sensor = sensor.sensor(self.id,str(self.id) + "sensor")
        self.getBS = False
        self.distance = []
        self.next_hop = []
        self.aggregate = []

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str("node"+str(self.id))

    def run(self):
        if self.id == 0: # if node is BS
            while True:
                if self.net.clock[0]=="CSMA":
                    print("at {0} BS is running".format(self.env.now))
                    yield self.env.timeout(config.BEACONING_TIME)

                elif self.net.clock[0]=="TDMA":
                    print("at {0} BS is calculating".format(self.env.now))
                    yield self.env.timeout(config.BEACONING_TIME)
                
                else:
                    print("BS is proccessing",self.env.now)
                    yield self.env.timeout(config.BEACONING_TIME)

        if self.id != 0: # if node is not BS
            while True:
                if(self.is_alive == True):
                    if (next(reversed(self.energy)) <= config.DEAD_NODE_THRESHOLD ):
                        print("^^^^^^^^^^node {0} is dead ith energy {1} at env:{2}^^^^^^^^^^^ \n".format(self.id,next(reversed(self.energy)),self.env.now))
                        if(self.is_CH == True):
                            print("ch is dead ,cluster needs to find another CH \n\n")
                            self.is_CH == False
                        self.is_alive = False
                        graphi = gui.graphic(self.net)
                        graphi.draw()
                if(self.is_alive == True):
                    if self.net.clock[0]=="TDMA":
                        print("TDMA ",self.net.TDMA_slot,config.TDMA_duration % self.net.TDMA_slot,config.TDMA_duration - self.net.TDMA_slot)
                        print("at {0} node {1} is working on TDMA {2} cluster {3} ".format(self.env.now,self.id,self.TDMA,self.cluster))
                        try:
                            if(self.is_alive == True):
                                yield self.env.process(self.TDMA_beaconing(self.env))
                        except simpy.Interrupt:
                            print("inter")
                        
                    elif self.net.clock[0]=="CSMA":
                        if(self.is_CH == True):
                            print("at %d CH talks in CSMA   %d "%(self.env.now,self.is_CH))

                        try:
                            if(self.is_alive == True):
                                yield self.env.process(self.CSMA_beaconing(self.env))
                        except simpy.Interrupt:
                            print("inter")

                    # else:
                    #     print("Inactive",self.env.now) # inactive time

                    if any("BS" in s for s in self.inbox):
                        self.BS_getter()
                        self.getBS == True
                        print(self,self.getBS,"bs is in inbox")
                    
                    # print(self.id, "test")

                    yield self.env.timeout(1)


    def CSMA_beaconing(self,env):
        message_sender = message.Message()
        if(self.is_alive == True): #if node is alive
            if len(self.parent) == 0: # if node has no parent ,beacons
                if(self.is_CH == False):
                    # yield self.env.timeout(1)
                    print("at {0} beacon CSMA adv is sent by {1} is alive {2}, since it has no CH with energy {3}".format(env.now,self.id,self.is_alive,self.power))
                    msg_len = message_sender.message_length()
                    self.power.decrease_tx_energy(msg_len)
                    self.energy.append(self.power.energy)

                    for n in self.neighbors:
                        message_sender.broadcast(n,"beacon CSMA adv {0} at env:{1}".format(n.id ,env.now))
                    yield self.env.timeout(1)

            if (self.is_CH == True): # if node is cluster head
                    # if(self.net.superframe_num % config )
                            self.power.decrease_energy(discharging_time = 100)  # idle discharge
                            self.node_send_message(self.aggregate,0)
                            self.aggregate.clear()
                            print("CH {0} aggregate CSMA sent to BS on env:{1}====+++++++++++++++++++ ".format(self.id,env.now))
                            # yield self.env.timeout(random.randint(1,config.AGGREGATE_TIME ))
                            yield self.env.timeout( random.randint(1, config.AGGREGATE_TIME +self.TDMA))
                            yield self.env.timeout(1)
        yield self.env.timeout(1)


    def TDMA_beaconing(self,env):
        message_sender = message.Message()
        if(self.is_alive == True): #if node is alive
            if (len(self.parent) != 0): # if node has parent send data to parent
                if self.TDMA != 0:
                    print(self.id,(self.net.TDMA_slot % self.TDMA))

                    if(((self.env.now % config.TDMA_duration)==self.TDMA )):
                        # print(self.id,"I have parent",self.TDMA,"at",self.env.now,"cluster",self.cluster)
                        print("at env:{3} light: {0} temperature: {1} from node {2} TDMA-based {4} to {5} with pos {6} {7} and parent {8}".format(self.sensor.light_sensor(),self.sensor.temperature_sensor(),self.id,env.now,self.TDMA,self.cluster,self.x,self.y,self.parent))

                        # yield self.env.timeout(config.CSMA_duration+config.Inactive_duration)
                        # if(self.parent[-1].is_alive == True):
                        # message_sender.send_message("at env:{3} light: {0} temperature: {1} from node {2} to {4}".format(self.sensor.light_sensor(),self.sensor.temperature_sensor(),self.id,env.now,self.parent[0]),self,self.parent[0])
                    msg_len = message_sender.message_length()
                    self.power.decrease_tx_energy(msg_len)
                    self.energy.append(self.power.energy)
        yield self.env.timeout(1)
            

    def node_send_message(self, str_message , node):
        #print("message {0} is sent^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ from {1} to {2}".format(str_message,self.id,node))
        self.outbox.append(str_message)


    def node_receive_message(self, str_message ,sender_node):
        self.inbox.append(str_message)
        if(self.is_CH == True): # if node is CH then aggregate
            self.aggregate.append(str_message)
        #self.send_ACK(sender_node)
        #print(self.id + " node_receive_message&&&&&&&&&&&&&&*************** " + str_message + " from "+ sender_node.name )
        if( "is cluster Head" in str_message ):
            # self.change_TDMA(sender_node.TDMA)
            self.parent_setter(sender_node)
            if(self.is_CH == True):
                self.change_CulsterHead()

        if( "BS" in str_message):
            if any("BS" in s for s in self.inbox):
                
                self.BS_getter()
                print("\n",self,self.getBS)
                print("distance is ",self.distance)
                print("for {0} neighbors are {1}".format(self,self.neighbors))
                time.sleep(1)
                for n in self.neighbors:
                    if n.id != 0:
                        print(n)

                        if n.distance != self.distance:
                            n.distance.append(self.distance)
                            n.distance.append(self)
                            print(n,"is neighbor ",self.id,n.distance)
                            if (len(n.distance)==0):
                                message1 = message.Message()
                                
                                message1.send_message("BS +{0}".format(self),self,n)
                                print(self,"message is sent to",n)
                                print(n.outbox ,n.id)
                                print(n.inbox ,n.id)
                
                # if self.id != 0:

                #     print("{0} get BS in message".format(self.id))
                #     time.sleep(3)
                #     for n in self.neighbors:
                #         if n.id != 0:
                #             if n.getBS == False:
                #                 n.getBS == True
                #                 print(n," get BS from ",self)
                #                 print(n.getBS,self.getBS)
                #                 if any("BS" in s for s in n.inbox):
                #                     print("temp inbox",self.id)
                #                     
        
    def send_ACK(self,destination_node):
        message1 = message.MyMessage()
        #message1.send_message("ack",cls,destination_node)

    def parent_setter(self,ch):
        self.parent.clear()
        self.parent.append(ch)
        #print(ch, "is head")

    def change_to_clusterhead(self):
        message_sender = message.Message()
        self.is_CH == True

    def add_nodes(self,list):
        self.neighbors.append(list)
        print(self.neighbors)


    def change_CulsterHead(self):
        if(self.is_CH == False):
            self.is_CH = True
            print("node {0} becomes CH (change)and parent is {1}".format(self.id,self.parent))
    
        else:
            self.is_CH == False
            self.next_hop.clear()
            print("node {0} becomes simple node (change) and parent is {1}".format(self.id,self.parent))

    def BS_getter(self):
        self.getBS == True