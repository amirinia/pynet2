import numpy as np 
import random 

def f(chromosome):
    print("ch",chromosome)
    return 0

def create_random():
        t1 = np.random.randint(low=4, high=7, size=1)
        t2 = np.random.randint(low=1, high=9, size=1)
        t3 = np.random.randint(low=0, high= 240 - t1 -t2, size=1)
        b1 = np.random.choice([0, 1])
        t = np.concatenate((t1, t2, t3, b1), axis=None)
        #print(t)
        return t
List = []
f(create_random())