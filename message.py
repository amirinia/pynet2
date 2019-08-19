#message
import node
import network
import packetloss


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
        for n in node.neighbors:
            message1 = Message ()
            message1.send_message(message,node,n)
            #message1.send_message(message,node,node.neighbors[x])

    def send_message(self, message , sender_node, destination_node):
        is_loss = packetloss.packetloss()
        sender_node.node_send_message(message,destination_node)
        self.data = message
            #destination_node.inbox.append(message)
        if(is_loss == True):
            destination_node.node_receive_message(message,sender_node)
            #node.node_receive_message(str_message,node)
            #print("message {0} is sent from {1} to {2}".format(message,sender_node.id,destination_node.id))
            #print("packet is lost",is_loss)

        elif(is_loss== False):
            sender_node.node_send_message(message + " resend",destination_node)
            destination_node.node_receive_message(message + " resend",sender_node)

            #print("packet is lost",is_loss)

        
    def send_beacon_message(self, energy, distance, rssi ,neighbor_tables , sender_node, destination_node):
        pass




    

