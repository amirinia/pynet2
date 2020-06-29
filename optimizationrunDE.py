import pandas as pd 
import numpy as np 
import random
import optimizationrun
D = 4
df = pd.DataFrame(columns=['pop','energy','duration','lost','dead'])

def function(x):
    op = optimizationrun
    a = op.run(x)
    global df
    df = df.append(pd.Series([x,a[0],a[1],a[2],a[3]], index=df.columns), ignore_index=True)

    return a[0]


""" DE """
De_FIT=[]
De_VAR=[]
De_POP=[]


population_num = 20
iteration = (D * 5000)/population_num

def de(fuctuion, mut=0.8, crossp=0.9, popsize=population_num, its=20):
        #print("de")
        dimensions = D
        initial = []
        for i in range(popsize):
            pop2 =[]
            t1 = random.randint(2,7)
            t2 = random.randint(2,9)
            t3 = random.randint((t1 +t2), 240 - (t1 +t2))
            b1 = random.choice([0, 1])
            pop2.append(t1)
            pop2.append(t2)
            pop2.append(t3)
            pop2.append(b1)

            initial.append(pop2)
        popnp = np.asarray(initial)
        #print((popnp))

        fitness = np.asarray([function(ind) for ind in popnp])
        #print("fitness list",fitness)
        best_idx = np.argmax(fitness)# find min or max
        #print("index of best",best_idx)
        best = popnp[best_idx]
        #print("best chromosome",best)
        for i in range(its):
            print(" New iteration ",i)
            for j in range(popsize):
                idxs = [idx for idx in range(popsize) if idx != j]
                #print(idxs)
                a, b, c = popnp[np.random.choice(idxs, 3, replace = False)]
                #print(a,b,c)
                mutant = np.clip(a + np.round( mut * (b - c)),0,237)#-1/(2-(1/(i+1))), 1/(2-(1/(i+1))))
                mutant = mutant.astype(int) # convert to int
                if(mutant[0] < 1):
                     mutant[0]=1 +random.randint(0,2)
                if(mutant[0] > 7):
                     mutant[0]=7 -random.randint(0,2)

                if(mutant[1] < 1):
                     mutant[1]=1 +random.randint(0,3)
                if(mutant[1] > 9):
                     mutant[1]=9 -random.randint(0,3)

                temp = mutant[1] + mutant[0]

                if(mutant[2] < temp):
                     mutant[2]=temp
                if(mutant[2] > 240 - temp):
                     mutant[2]= 240 - temp

                if(mutant[3] < 0):
                     mutant[3]=0
                if(mutant[3] > 1):
                     mutant[3]=1
                print("mutant",mutant)

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
            
            #De_FIT.append(fitness[best_idx])
            #De_VAR.append(best)

        print("best  ",best,fitness[best_idx])
        return best, fitness[best_idx]


de(lambda x: function(x))
#print("fit ",De_FIT," ide ",De_VAR," ",De_POP)
df.to_csv('report/DE best 2020-10-10.csv')

