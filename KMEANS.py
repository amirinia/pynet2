import network
import simpy
import random
import config
import node
import gui

k = 3
env = simpy.Environment()
net1 = network.Net(env)
net1.random_net_generator(env,net1,10)

#print(net1.nodes[0].x)

def Kmeans(network,itrations):

    for n in net1.nodes:
        distance = config.AREA_WIDTH
        #print(net1.distance(n,nodech))
        for i in range(itrations):
        
            x=random.randint(0,config.AREA_WIDTH)
            y=random.randint(0,config.AREA_LENGTH)
            nodech = node.Node(1000+i,env,2,x,y)
            
            #print(i,x,y)
            if(distance > net1.distance(n,nodech)):
                distance = net1.distance(n,nodech)
                print(n,nodech,distance)
                n.parent.clear()
                n.parent.append(nodech)



Kmeans(net1,5)
net1.introduce_yourself()
graphi = gui.graphic(net1)
graphi.draw_ch()