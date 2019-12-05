import pandas as pd 
import numpy as np 
import random

D = 9

def function(x):
    #print(x[0],+x[1],x[0]+x[1])
    return x[0]+x[1]

""" DE """
De_FIT=[]
De_VAR=[]
De_POP=[]


def de(fuctuion, mut=0.8, crossp=0.9, popsize=100, its=10):
        #print("de")
        dimensions = D
        initial = []
        for i in range(popsize):
            pop = np.random.randint(low=1,high=10,size=dimensions)
            #print("pop ",pop)
            initial.append(pop)
        popnp = np.asarray(initial)
        print((popnp))

        fitness = np.asarray([function(ind) for ind in popnp])
        print("fitness list",fitness)
        best_idx = np.argmin(fitness)
        print("index of best",best_idx)
        best = popnp[best_idx]
        print("best chromosome",best)
        for i in range(its):
             for j in range(popsize):
                 idxs = [idx for idx in range(popsize) if idx != j]
                 #print(idxs)
                 a, b, c = popnp[np.random.choice(idxs, 3, replace = False)]
                 #print(a,b,c)
                 mutant = np.clip(a +np.round( mut * (b - c)),0,100)#-1/(2-(1/(i+1))), 1/(2-(1/(i+1))))
                 #print("mutant",mutant)
                 cross_points = np.random.rand(dimensions) < crossp
                 #print(cross_points)
                 if not np.any(cross_points):
                     cross_points[np.random.randint(0, dimensions)] = True
                 trial = np.where(cross_points, mutant, popnp[j])
                 #print("trail",trial)
    
                 f = function(trial)
                 if f < fitness[j]:
                     fitness[j] = f
                     popnp[j] = trial
                     if f < fitness[best_idx]:
                         best_idx = j
                         best = trial
            
             De_FIT.append(fitness[best_idx])
             De_VAR.append(best)
             return best, fitness[best_idx]


de(lambda x: function(x) ,its=50)
print("list",De_FIT,De_VAR)