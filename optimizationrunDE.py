import pandas as pd 
import numpy as np 
import random
#import network as initialieee802154
import gui
import config
import report
import logger
import simpy
import ieee802154
from node import Node
import LEACH 
import clusteringKMEANS as KMEANS
import pickle
import time
import datetime

config.printenabled = False
config.guienabled = False
t1 = datetime.datetime.now()
print(time.ctime)
# here you select if it start with statci ieee802154 or ieee802154 maker
startstatic = False
# in second step you need and algorithm
second = False

population_num = 33
iteration = 33


print("\nStatic network is {0} and Kmeans is {1} and Max run time is {2} @ {3}".format(startstatic,second,config.MAX_RUNTIME,time.ctime()))


def run(x):

     config.TDMA_duration = x[0]
     config.CSMA_duration = x[1]
     config.Inactive_duration = x[2]
     if x[3] ==0:
        config.Multiframe_state = True
     else:
        config.Multiframe_state = False


     # here you select if it start with statci ieee802154 or ieee802154 maker
     if(startstatic):
          # import network as initialieee802154
          # ieee1 = initialieee802154.ieee1
          # env = initialieee802154.env
          env = simpy.Environment()

          ieee1 = ieee802154.Net(env)

          ieee1.add_node(Node(0, env, 4, (config.xsize)/2, (config.ysize)/2, node_type='B' ,power_type=0,ieee802154 =ieee1))
          ieee1.add_node(Node(1,env,1.99, 10,10,ieee802154 =ieee1))
          ieee1.add_node(Node(2,env,1.98,10,60,ieee802154 =ieee1, sensor_type=1))
          ieee1.add_node(Node(3,env,1.988,30,11,ieee802154 =ieee1))
          ieee1.add_node(Node(4,env,1.9088,43,35,ieee802154 =ieee1, sensor_type=1))
          ieee1.add_node(Node(5,env,1.9855,260,30,ieee802154 =ieee1))
          ieee1.add_node(Node(6,env,1.9678,270,50,ieee802154 =ieee1, sensor_type=1))
          ieee1.add_node(Node(7,env,1.8434,259,72,ieee802154 =ieee1))
          ieee1.add_node(Node(8,env,1.90234,241,47,ieee802154 =ieee1, sensor_type=1))
          ieee1.add_node(Node(9,env,1.989364,260,200,ieee802154 =ieee1))
          ieee1.add_node(Node(10,env,1.876549,290,200,ieee802154 =ieee1, sensor_type=1))
          ieee1.add_node(Node(11,env,1.78233 ,280,220 ,ieee802154 =ieee1))
          ieee1.add_node(Node(12,env,1.79745,20,200,ieee802154 =ieee1 , sensor_type=1))
          ieee1.add_node(Node(13,env,1.86435,10,160,ieee802154 =ieee1 ))
          ieee1.add_node(Node(14,env,1.76434 ,13,183,ieee802154 =ieee1, sensor_type=1))
          ieee1.add_node(Node(15,env,1.9754734 ,50,200,ieee802154 =ieee1 ))
          ieee1.add_node(Node(16,env,1.8634754 ,29,189,ieee802154 =ieee1, sensor_type=1 ))
          ieee1.add_node(Node(17,env,1.87648 ,35,204,ieee802154 =ieee1))
          ieee1.add_node(Node(18,env,1.7645,31,172,ieee802154 =ieee1, sensor_type=1 ))
          ieee1.add_node(Node(19,env,1.3654675,30,50,ieee802154 =ieee1 ))
          ieee1.add_node(Node(20,env,1.846 ,130,20,ieee802154 =ieee1 , sensor_type=1))
          ieee1.add_node(Node(21,env,1.786487,135,2,ieee802154 =ieee1))
          ieee1.add_node(Node(22,env,2 ,175,5,ieee802154 =ieee1, sensor_type=1))


     else:
          positions =[]
          positions = pickle.load(open("report/pos.pickle", "rb"))
          env = simpy.Environment()
          ieee1 = ieee802154.Net(env)
          ieee1.add_node(Node(0, env, 4, (config.xsize)/2, (config.ysize)/2, node_type='B' ,power_type=0,ieee802154 =ieee1))
          for i in range(len(positions)):
               if (i >0):
                    x = positions[i][0]
                    y = config.ysize - positions[i][1]
                    #print("p = x:",positions[i][0],positions[i][1],i)
                    if (i % 2== 0):
                         ieee1.add_node(Node(i,env,2000,x,y,ieee802154=ieee1 ))
                    else:
                         ieee1.add_node(Node(i,env,2000,x,y,ieee802154=ieee1, sensor_type=1 ))
     




     ieee1.introduce_yourself()
     ieee1.ieee802154_nodedsicovery()



     if config.printenabled:

          print("_____________________________Clustering Algorithm___________________________________ start\n\n")
     if(second):
        KMEANS1 = KMEANS.Kmeans(env,ieee1,10)
        #print("KMEANS")
     else:
        LEACH1 = LEACH.LEACHC(env,ieee1)
        #print("LEACH")
     if config.printenabled:

          print("_____________________________Clustering Algorithm___________________________________ end\n\n")


          print("++++++++++++++++++++++++++++++++++++++++++++++++++")
     ieee1.introduce_yourself()
     if(config.guienabled):
          graphi = gui.graphic(ieee1)
          graphi.draw_neighbors()
          graphi.draw()
    #graphi.draw()
    #logger.logger.log(str("++++++++++++++++++++++++++++++++++++++++++++++++++ run begin ++++++++++++++++++++++++"))

     if config.printenabled:

          print("++++++++++++++++++++++++++++++++++++++++++++++++++ run begin ++++++++++++++++++++++++")
     env.run(until=config.MAX_RUNTIME)
    #logger.logger.log(str("++++++++++++++++++++++++++++++++++++++++++++++++++ run end ++++++++++++++++++++++++"))
     if config.printenabled:

          print("++++++++++++++++++++++++++++++++++++++++++++++++++ run end ++++++++++++++++++++++++")


     ieee1.ieee802154_packet_summery()

     ieee1.introduce_yourself()   

     a = ieee1.ieee802154_optimize()
    #df = df.append(pd.Series([x,a[0],a[1],a[2],a[3]], index=df.columns), ignore_index=True)

     return a






D = 4
df = pd.DataFrame(columns=['pop','energy','duration','lost','dead'])
#iteration = (D * 5000)/population_num

def function(x):
     a = run(x)
     global df
     df = df.append(pd.Series([x,a[0],a[1],a[2],a[3]], index=df.columns), ignore_index=True)
     print("choromosome ",x," remaining energy: ",a[0])
     return a[0]


# """ DE """
# De_FIT=[]
# De_VAR=[]
# De_POP=[]



def de(fuctuion, mut=0.8, crossp=0.9, popsize=population_num, its=iteration):
        print("DE starts with population: {0} and itration: {1}  [TDMA, CSMA, Inactive, Multi]".format(popsize,its))
        dimensions = D
        maxduration = 15625 #240 #Change 1 second to 15.36 ms time slot  4 min ==> 240,000 ms /15.36 => 15,625 number of slots Pass bayad max duration beshe 15,625 slot
        initial = []
        for i in range(popsize):
            pop2 =[]
            t1 = random.randint(2,7)
            t2 = random.randint(2,9)
            tempmin = (t1 + t2) 
            t3 = random.randint(0, maxduration - tempmin)
            b1 = random.choice([0, 1])
            pop2.append(t1)
            pop2.append(t2)
            pop2.append(t3)
            pop2.append(b1)

            initial.append(pop2)
        popnp = np.asarray(initial)
        #print((popnp))
        df = pd.DataFrame(columns=['pop','energy','duration','lost','dead'])

        fitness = np.asarray([function(ind) for ind in popnp])
        #print("fitness list",fitness)
        best_idx = np.argmax(fitness)# find min or max
        #print("index of best",best_idx)
        best = popnp[best_idx]
        print("\n Best chromosome",best , best_idx)
        previousbest = ""
        for i in range(its):

            print("\n New iteration ",i+1 , " ",time.ctime())
            for j in range(popsize):
                idxs = [idx for idx in range(popsize) if idx != j]
                #print(idxs)
                a, b, c = popnp[np.random.choice(idxs, 3, replace = False)]
                #print(a,b,c)
                mutant = np.clip(a + np.round( mut * (b - c)),0,maxduration)#-1/(2-(1/(i+1))), 1/(2-(1/(i+1))))
                mutant = mutant.astype(int) # convert to int
                if(mutant[0] < 1):
                     mutant[0]=1 + random.randint(0,2)
                if(mutant[0] > 7):
                     mutant[0]=7 - random.randint(0,2)
                if(mutant[1] < 1):
                     mutant[1]=1 + random.randint(0,3)
                if(mutant[1] > 9):
                     mutant[1]=9 - random.randint(0,3)

                #temp = mutant[1] + mutant[0] + round(maxduration/10)

                if(mutant[2] < 16):
                     mutant[2]=  random.randint(0,15000)
                if(mutant[2] > maxduration - tempmin):  #
                     mutant[2]= maxduration - tempmin - random.randint(0,10000)

                if(mutant[3] < 0):
                     mutant[3]=0
                if(mutant[3] > 1):
                     mutant[3]=1
                #print("mutant",mutant)

                cross_points = np.random.rand(dimensions) < crossp
                #print(cross_points)
                if not np.any(cross_points):
                     cross_points[np.random.randint(0, dimensions)] = True
                trial = np.where(cross_points, mutant, popnp[j])
                 #print("trail",trial)
                 

                f = function(trial)
                if f > fitness[j]:
                     fitness[j] = f 
                     popnp[j] = trial
                     if f > fitness[best_idx]:
                         best_idx = j
                         best = trial
                         print("Best", best)
                     if f == fitness[best_idx]:
                         print("equal with previous", previousbest)
                         previousbest = best
            #De_FIT.append(fitness[best_idx])
            #De_VAR.append(best)

        print("best  ",best,fitness[best_idx])
        return best, fitness[best_idx]
        #df.to_csv('report/DE best 2020-20-20.csv') # just last iteration
        #df.append(df2, ignore_index=True)

de(lambda x: function(x))
#print("fit ",De_FIT," ide ",De_VAR," ",De_POP)
t2 = datetime.datetime.now()

print(time.ctime())
print(t1 - t2)
df.to_csv('report/DE best 2020LE-{0}-{1}-{2}-{3}.csv'.format(population_num,iteration,startstatic,second))