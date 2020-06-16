import simpy
import network 
from  node import  Node
import message
import time
import gui
import config
import pickle
import io

positions =[]


positions = pickle.load(open("pos.pickle", "rb"))


def makeinitialnetwork(positions):
        env = simpy.Environment()
        net1 = network.Net(env)
        print(positions)
        for i in range(len(positions)):
            print(i)
            if (i >0):
                print("p= ",positions[i][0],positions[i][1],i)

                net1.add_node(Node(i,env,2000,positions[i][0],positions[i][1],node_type=None,network=net1))
        net1.introduce_yourself()
        print("KKKKKKKKKK")
        #net1.network_nodedsicovery()
        
        # listnodes = net1.nodes
        # file_pi = open('linstnodes.obj', 'w') 
        # pickle.dump(listnodes, file_pi)
        # with open('net1.pkl', 'wb') as handle:
        #     pickle.dump(net1, handle)
        #pickle.dump(net1, file = open("net1.pickle", "wb"))
        # reloaded1 = pickle.load(open("net1.pickle", "rb"))
        
        graphi = gui.graphic(net1)
        graphi.draw_nods()

makeinitialnetwork(positions)
print( pickle.load(open("nodelist.pickle", "rb")))
