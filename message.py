#message
import node
import network
import packetloss
import energymodel
from propagation import PropagationModel
import math
from interference import  Interference


Message_Type = {0: "Broadcast", 1: "Data", 2: "Ack",3: "Beacon" ,4: "Single"}

class Message(object):

    def __init__(self,data={}, source=None, destination=None, nexthop=None, header=''):
        """
        pymote 2
        """
        self.source = source
        self.destination = destination
        self.nexthop = nexthop
        self.header = header
        self.data = data
        self.overhead_bytes = 60

    def message_length(self):
        return len(self.header + str(self.data)) + self.overhead_bytes
        """
        pymote 2
        """

    def broadcast(self,node,message="hello"):
        message_sender = Message(message)
        msg_len = message_sender.message_length()
        for n in node.neighbors:
            message_sender.send_message(message,node,n)
            
            #message1.send_message(message,node,node.neighbors[x])
        
        # energy cosumption for receiving tx  decrease
        node.power.decrease_tx_energy(msg_len)
        node.energy.append(node.power.energy)



    def send_message(self, message , sender_node, destination_node, TDMA = False):
        if(sender_node.is_alive == True):
            #is_loss = packetloss.packetloss() # packet loss model

            # propagation model
            en = PropagationModel(propagation_type=1)
            n = sender_node
            n1 = destination_node
            d = math.sqrt(((n.x-n1.x)**2)+((n.y-n1.y)**2))
            prt = en.get_power_ratio(d=d)
            rx_ok = en.is_rx_ok(d=d, prt=prt)
            sender_node.node_send_message(message,destination_node)

            self.data = message
                #destination_node.inbox.append(message)
            if(rx_ok == True): # if no lost
                destination_node.node_receive_message(message,sender_node)
                destination_node.node_send_message("ACK ",sender_node)
                sender_node.node_receive_message("ACK " ,destination_node)
                #node.node_receive_message(str_message,node)
                #print("message {0} is sent from {1} to {2}".format(message,sender_node.id,destination_node.id))
                #print("packet is lost",is_loss)

                message_sender = Message(message)
                msg_len = message_sender.message_length()

                self.decreasEngryrx(destination_node,msg_len)

            elif(rx_ok== False):
                sender_node.node_send_message(message + " resend",destination_node)
                destination_node.node_receive_message(message + " resend",sender_node)
                destination_node.node_send_message("ACK "  + " resend",sender_node)
                sender_node.node_receive_message("ACK ",destination_node)

                self.decreasEngryrx(destination_node,msg_len)
                self.decreasEngryrx(destination_node,msg_len)


                #print("packet is lost",is_loss)

    def decreasEngryrx(self,destination_node,msg_len):
        # energy cosumption for receiving rx  decrease
        destination_node.power.decrease_rx_energy(msg_len)
        destination_node.energy.append(destination_node.power.energy)


    def send_beacon_message(self, energy, distance, rssi ,neighbor_tables , sender_node, destination_node):
        pass




    

