import simpy
import ieee802154
import random 
import config
import message
from energymodel import EnergyModel
import time
import gui
import cluster
import math
import pandas as pd 
import logger
import sys
from superframe import Superframe
from interference import Interference



Sensor_Type = {0: "Alert-Temperature", 1: "Monitoring"}
class sensor:
    def __init__(self,id,name,Sensor_Type=1):
        self.id = id
        self.name = name
        self.sensor_type = Sensor_Type

    def __str__(self):
        return str(self.sensor_type)

    def __repr__(self):
        return str("sensor"+str(self.sensor_type))

    def run(self,env):
        if self.sensor_type == 0:
            if config.printenabled:
                print(self.temperature_sensor())
        if config.printenabled:
            print(self.light_sensor())
            print(self.temperature_sensor())

    def temperature_sensor(self):
        return random.randint(17,30)
        
    def light_sensor(self):
        return random.randint(100,300)

    def humidity_sensor(self):
        return random.randint(171 , 194)

class Node():
    def __init__(self,id,env,energy=(config.INITIAL_ENERGY-random.randint(1000,2000)),x=random.randint(0,config.AREA_WIDTH),y=random.randint(0,config.AREA_LENGTH),node_type=None, power_type=1, mobile_type=0, ieee802154=ieee802154 ,sensor_type=0):
        self.env = env
        self.id = id
        self.net = ieee802154
        self.is_alive = True
        self.energy = [energy]
        #print("node is created ")
        self.is_CH = False
        self.x = x
        self.y = y
        self.neighbors = []
        self.inbox = []
        self.outbox = []
        self.buffer =[]
        self.parent = []
        self.clus = cluster
        self.cluster = []
        self.TDMA = 0
        self.power = EnergyModel(power_type = power_type)
        self.sensor = sensor(self.id,str(self.id) + "sensor",sensor_type)
        self.getBS = False
        self.distance = []
        self.next_hop = []
        self.aggregate = []
        self.light = 0
        self.temperature = 0 
        self.alert_neighbor = False
        self.logger = logger.logger()
        self.deadtime = 100000000000000
        self.superframe = Superframe()
        #self.interfrerence = Interference(self.env)
        self.flag = False
        self.action = env.process(self.run())

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str("node"+str(self.id))

    def run(self):
        if self.id == 0: # if node is BS
            df = pd.DataFrame(columns=['id','deadtime','remainedenergy'])

            while True:
                self.flag = False
                self.parent.clear()

                if self.net.clock[0]=="CSMA":
                    self.logger.log("at {0} BS is running".format(self.env.now))
                    if config.printenabled:
                        print("at {0} BS is running".format(self.env.now))
                    yield self.env.timeout(config.BEACONING_TIME)

                elif self.net.clock[0]=="TDMA":
                    self.logger.log("at {0} BS is calculating".format(self.env.now))
                    if config.printenabled:
                        print("at {0} BS is calculating".format(self.env.now))
                    yield self.env.timeout(config.BEACONING_TIME)
                
                else:
                    self.logger.log("BS is proccessing {0}".format(self.env.now))
                    #if config.printenabled:
                        #print("BS is proccessing {0}".format(self.env.now))
                    yield self.env.timeout(config.BEACONING_TIME)
        if (next(reversed(self.energy)) <= config.DEAD_NODE_THRESHOLD):
            self.is_alive = False

        if self.id != 0: # if node is not BS
            while True:
                self.flag = False
                # if(len(self.parent)!=0 and self.parent[0].is_CH == False):
                #     self.parent.clear()
                if(self.is_alive == True):
                    if (next(reversed(self.energy)) <= config.DEAD_NODE_THRESHOLD ):
                        if(self.is_alive == True):
                            self.is_alive == False
                        self.logger.log("^^^^^^^^^^node {0} is dead ith energy {1} at env:{2}^^^^^^^^^^^ \n".format(self.id,next(reversed(self.energy)),self.env.now))
                        # if config.printenabled:
                        print("^^^^^^^^^^node {0} is dead ith energy {1} at env:{2}^^^^^^^^^^^ \n".format(self.id,next(reversed(self.energy)),self.env.now))
                        print(self.power.energy)
                        #print(self.clus)

                        self.deadtime = self.env.now
                        
                        #self.clus.mycluster.Clusterhead_Selection()#SRandom_Clusterhead_Selection()
                        self.env.timeout(100)
                        yield self.env.timeout(10)


                        #self.net.savedeadnodes(self.id,next(reversed(self.energy)),self.env.now)
                        if(self.is_CH == True):
                            self.logger.log("ch is dead ,cluster needs to find another CH {0} {1}\n\n".format(self.env.now, config.Duration))
                            if config.printenabled:
                                print("ch is dead ,cluster needs to find another CH {0} {1}\n\n".format(self.env.now, config.Duration))
                            self.is_CH == False
                            if config.printenabled:
                                print("cc test {0} cluster{1} size {2}".format(self.cluster,"ooo","cluster head is dead"))
                            #self.clus.mycluster.Clusterhead_Selection(self.cluster.self)
                            
                            #self.cluster.Clusterhead_Selection()
                        self.is_alive = False
                        # draw
                        #time.sleep(4)
                        if(config.guienabled):

                            #graphi = gui.graphic(self.net)
                            #graphi.drawdead("{0} {1}".format(self.id ,self.env.now ))
                            # save dead
                            graph = gui.graphic(self.net)
                            graph.draw()
                        if config.printenabled:
                            print("env exit")
                        # self.net.env.exit()
                        # sys.exit()

                    # if self.env.now > config.ALERT_TIME:
                    #     if self.net.alert :
                    #          if(config.Alert_RANGE > math.sqrt(((config.alertx-self.x)**2)+((config.alerty-self.y)**2))):
                    #              self.alert_neighbor = True
                    #     else:
                    #              self.alert_neighbor = False


                    if self.net.clock[0]=="TDMA":
                        #print(self.net.TDMA_slot,(self.TDMA))
                        if(self.is_CH == False):
                            if(config.TDMA_duration < (self.TDMA )): # there is no TDMA for this onde in ieee802154
                                if config.printenabled:
                                    print("TDMA of this nod does not exist node : ", self.id)
                                self.power.decrease_tx_energy(10000)
                                self.energy.append(self.power.energy)



                            if(self.net.TDMA_slot -1 == (self.TDMA )):
                                if(len(self.parent)!=0):
                                    #print(self.net.TDMA_slot,(self.TDMA))

                                    temp1 =""
                                    #self.flag = True
                                    if(not self.alert_neighbor):
                                        self.light = self.sensor.light_sensor()
                                        # self.cluster[0].light.append(self.light)
                                        self.temperature = self.sensor.temperature_sensor()
                                        # self.cluster[0].temperature.append(self.temperature)
                                    elif(self.alert_neighbor):
                                        self.light = config.Alert_increase_temp+ self.sensor.light_sensor()
                                        # self.cluster[0].light.append(self.light)
                                        temp1 = str(self.id) + " Alert " 
                                        # send alert to BS
                                        self.temperature = 200+ self.sensor.temperature_sensor()
                                        # self.cluster[0].temperature.append(self.temperature)
                                    if(config.Multiframe_state):
                                        if(self.sensor.sensor_type == 1 and self.net.superframe_num % config.Multiframe_size == 0): # every 2 superframe  Multisuperframe
                                            tempmessage = temp1 + "at env:{3} from node t1 {2} light: {0} temperature: {1} TDMA-based {4} to {5} with pos {6} {7} and parent {8} and energy {9}".format(self.light,self.temperature,self.id,self.env.now,self.TDMA,self.cluster,self.x,self.y,self.parent,next(reversed(self.energy)))
                                            self.logger.log(tempmessage)
                                            if config.printenabled:
                                                print(tempmessage)
                                            message_sender = message.Message(tempmessage)
     
                                            message_sender.send_message(tempmessage,self,self.parent[0],TDMA=True)
                                            self.parent[0].buffer.append(tempmessage)

                                        if (self.sensor.sensor_type == 0): # every frame nodetype
                                            tempmessage = temp1 + "at env:{3} from node t0 {2} light: {0} temperature: {1} TDMA-based {4} to {5} with pos {6} {7} and parent {8} and energy {9}".format(self.light,self.temperature,self.id,self.env.now,self.TDMA,self.cluster,self.x,self.y,self.parent,next(reversed(self.energy)))
                                            self.logger.log(tempmessage)
                                            if config.printenabled:
                                                print(tempmessage)
                                            message_sender = message.Message(tempmessage)

                                            message_sender.send_message(tempmessage,self,self.parent[0],TDMA=True)
                                            self.parent[0].buffer.append(tempmessage)
                                        #self.interference.listsetter(self.id)

                                    else:
                                        tempmessage = temp1 + "at env:{3} from node {2} light: {0} temperature: {1} TDMA-based {4} to {5} with pos {6} {7} and parent {8} and energy {9}".format(self.light,self.temperature,self.id,self.env.now,self.TDMA,self.cluster,self.x,self.y,self.parent,next(reversed(self.energy)))
                                        self.logger.log(tempmessage)
                                        if config.printenabled:
                                            print(tempmessage)
                                        message_sender = message.Message(tempmessage)

                                        message_sender.send_message(tempmessage,self,self.parent[0],TDMA=True)
                                        self.parent[0].buffer.append(tempmessage)
                                        #self.interference.listsetter(self.id)


                                
                                    
                            # try:
                            #     if(self.is_alive == True):
                            #         yield self.env.process(self.TDMA_beaconing(self.env))
                            # except simpy.Interrupt:
                            #     print("inter")
                        
                    elif self.net.clock[0]=="CSMA":
                            # print("at %d CH %d talks in CSMA   %d "%(self.env.now,self.id,self.is_CH))

                            try:
                                if(self.is_alive == True):
                                    yield self.env.process(self.CSMA_beaconing(self.env))
                            except simpy.Interrupt:
                                if config.printenabled:
                                    print("inter")

                    # else:
                    #     print("Inactive",self.env.now) # inactive time
                    if self.net.clock[0]=="CSMA" and self.net.clock[0]=="TDMA" :
                        if any("BS" in s for s in self.inbox):
                            self.BS_getter()
                            self.getBS == True
                            self.logger.log("{0} {1} {2}".format(self.id,self.getBS,"bs is in inbox"))
                            if config.printenabled:
                                print("{0} {1} {2}".format(self.id,self.getBS,"bs is in inbox"))
                        
                    # print(self.id, "test")

                    yield self.env.timeout(1)
            #if (next(reversed(self.energy)) <= config.DEAD_NODE_THRESHOLD):
                #self.is_alive = False
                #print("node isdead...."+self.id)
                #yield self.env.timeout(10)

    def CSMA_beaconing(self,env):
        if(self.is_alive == True): #if node is alive
            if len(self.parent) == 0: # if node has no parent ,beacons
                if(self.is_CH == False):
                    if(random.randint(1,config.CSMA_duration)==5):

                        tempmessage = "at {0} beacon CSMA adv is sent by {1} aprent is {2}, since it has no CH with energy {3}".format(env.now,self.id,self.parent,self.power)
                        self.logger.log(tempmessage)
                        if config.printenabled:
                            print(tempmessage)
                        message_sender = message.Message(tempmessage)
                        #self.flag = True


                        for n in self.neighbors:
                            message_sender.broadcast(n,"beacon CSMA adv {0} at env:{1}".format(n.id ,env.now),n.neighbors)
                            yield self.env.timeout(1)

            if (self.is_CH == True): # if node is cluster head
                # print(random.randint(1,config.CSMA_duration))
                if(random.randint(1,config.CSMA_duration)==5):
                    if len(self.buffer) !=0 :
                            # self.power.decrease_energy(discharging_time = 10)  # idle discharge
                            tempbuffer = "CH {0} aggregate CSMA sent to BS on env:{1}====+++++++++++++++++++\n {2} ".format(self.id,env.now,self.buffer)
                            tempbuffer += "at env:{3} from node {2} light: {0} temperature: {1} TDMA-based {4} to {5} with pos {6} {7} and parent {8}".format(self.light,self.temperature,self.id,self.env.now,self.TDMA,self.cluster,self.x,self.y,self.parent)
                            # message_sender.send_message(temp,self,self.net.nodes[0])
                            self.net.nodes[0].inbox.append(tempbuffer)
                            self.node_send_message(self.aggregate,0)
                            self.aggregate.clear()
                            self.logger.log(tempbuffer)
                            if config.printenabled:
                                print(tempbuffer)
                            # energy tx decrease
                            message_sender = message.Message(tempbuffer)
                                        #self.interference.listsetter(self.id)

                            self.buffer.clear()
                            #self.flag = True

                            # print(self.clus.cluster_average_light())
                            # self.clus.light.clear()

        # yield self.env.timeout(1)


    def TDMA_beaconing(self,env):
        print(" TT node",self.id,self.is_CH,self.TDMA)

    #     message_sender = message.Message()
    #     if(self.is_alive == True): #if node is alive
    #         if (len(self.parent) != 0): # if node has parent send data to parent
    #             if self.TDMA != 0:
    #                 print("this node can work ",self.id,(self.net.TDMA_slot % self.TDMA),self.net.TDMA_slot==self.TDMA+1,self.TDMA+1)

    #                 if(self.net.TDMA_slot==self.TDMA+1):
    #                     # print(self.id,"I have parent",self.TDMA,"at",self.env.now,"cluster",self.cluster)
    #                     tempmessage = "at env:{3} from node {2} light: {0} temperature: {1} TDMA-based {4} to cluster {5} with pos {6} {7} and parent {8}".format(self.sensor.light_sensor(),self.sensor.temperature_sensor(),self.id,env.now,self.TDMA,self.cluster,self.x,self.y,self.parent)
    #                     print(tempmessage)
    #                     # yield self.env.timeout(config.CSMA_duration+config.Inactive_duration)
    #                     # if(self.parent[-1].is_alive == True):
    #                     # message_sender.send_message("at env:{3} light: {0} temperature: {1} from node {2} to {4}".format(self.sensor.light_sensor(),self.sensor.temperature_sensor(),self.id,env.now,self.parent[0]),self,self.parent[0])
    #                 msg_len = message_sender.message_length()
  
        yield self.env.timeout(1)
            

    def node_send_message(self, str_message , node):
        #print("message {0} is sent^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ from {1} to {2}".format(str_message,self.id,node))
        self.outbox.append(str_message)
        



    def node_receive_message(self, str_message ,sender_node):
        self.inbox.append(str_message)
        self.flag = True
        if(self.is_CH == True): # if node is CH then aggregate
            self.aggregate.append(str_message)
        #self.send_ACK(sender_node)
        #print(self.id + " node_receive_message&&&&&&&&&&&&&&*************** " + str_message + " from "+ sender_node.name )
        # if(self.header == 'superframe'):
        #     print("zzzzzzzzzz")
        #     exit()
        if("ACK" in str_message ):   
            self.flag = False

        if("Superframe rules" in str_message ):
            if config.printenabled:
                print("superframe is set on node {0}".format(self.id))
        
    
        if( "is cluster Head" in str_message ):
            if (sender_node.cluster == self.cluster):
                self.parent_setter(sender_node)
                if(self.is_CH == True):
                    self.parent_setter(sender_node)

                    self.change_CulsterHead()

                    self.is_CH = False
                    if config.printenabled:
                        print("node {0} is CH NOW nnn parent is {1} and node is CH {2}".format(self.id, self.parent,self.is_CH))




        if( "BS" in str_message):
            if any("BS" in s for s in self.inbox):
                
                self.BS_getter()
                #print("\n",self,self.getBS, "is CH ",self.is_CH)
                #print("distance is ",self.distance)
                #self.logger.log("for {0} neighbors are {1}".format(self,self.neighbors))
                #print("for {0} neighbors are {1}".format(self,self.neighbors))
                # time.sleep(1)
                # for n in self.neighbors:
                #     if n.id != 0:
                #         print(n)

                #         if n.distance != self.distance:
                #             n.distance.append(self.distance)
                #             n.distance.append(self)
                #             print(n,"is neighbor ",self.id,n.distance)
                #             if (len(n.distance)==0):
                #                 message1 = message.Message()
                                
                #                 message1.send_message("BS +{0}".format(self),self,n)
                #                 print(self,"message is sent to",n)
                #                 print(n.outbox ,n.id)
                #                 print(n.inbox ,n.id)
                
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
        # if( "Alert" in str_message): 
        #     print("fire 2 sould be siezed \n\n",self.id)                 
        #     print(self.id)
        #     if self.id == 0:
        #         print("fire 1 sould be siezed \n\n",self.id)                 
        
    def send_ACK(self,destination_node):
        message1 = message.MyMessage()
        #message1.send_message("ack",cls,destination_node)

    def parent_setter(self,ch):
        self.parent.clear()
        if(self.id !=0):
            self.parent.append(ch)
        #print(ch, "is head")


    def add_nodes(self,list):
        self.neighbors.append(list)
        if config.printenabled:
            print(self.neighbors)


    def change_CulsterHead(self):
        if(self.is_CH == False and self.id !=0):
            self.is_CH = True
            self.parent.clear()

            self.logger.log("node {0} becomes CH (change)and parent is {1} and TDMA {2} energy {3}".format(self.id,self.parent,self.TDMA,(next(reversed(self.energy)))))
            if config.printenabled:
                print("node {0} becomes CH (change)and parent is {1} and TDMA energy {3}".format(self.id,self.parent,self.TDMA,(next(reversed(self.energy)))))
            self.distance.clear
            self.distance.append(self.net.nodes[0])
        if(self.is_CH == True and self.id !=0):
            self.is_CH == False
            self.next_hop.clear()
            self.logger.log("e node {0} becomes simple node (change) and parent is {1} and TDMA {2} energy {3}".format(self.id,self.parent,self.TDMA,(next(reversed(self.energy)))))
            if config.printenabled:
                print("e node {0} becomes simple node (change) and parent is {1} and TDMA {2} energy {3}".format(self.id,self.parent,self.TDMA,(next(reversed(self.energy)))))
            #self.distance.append(next(reversed(self.parent)))

    def BS_getter(self):
        self.getBS == True

    def set_TDMA(self,num):
        self.TDMA = num

    def alert_toggle(self):
        self.alert_neighbor == True