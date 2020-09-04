import numpy as np 
import random 

def f(numbers):
    return np.sum(numbers)

class Particle:
    def __init__(self):
        self.id = id
        self.positions = self.create_random()
        self.localbest = self.positions
        self.velocity = random.randint(-2, 2)

    def create_random(self):
        t1 = np.random.randint(low=4, high=7, size=1)
        t2 = np.random.randint(low=1, high=9, size=1)
        t3 = np.random.randint(low=0, high= 240 - t1 -t2, size=1)
        b1 = np.random.choice([0, 1])
        t = np.concatenate((t1, t2, t3, b1), axis=None)
        print(t)
        return t


class MyPSO():
    def __init__(self,particlenumber):
        self.gbest = self.create_random()
        self.particles = []
        self.bestlist = []
        for i in range(particlenumber):
            p = Particle()
            
            self.particles.append(Particle())
            if f(self.gbest) > f(p.positions) :
                print(f(self.gbest) > f(p.positions))
                print(f(self.gbest),"global =>",f(p.positions))
                self.gbest = p.positions
    
    def create_random(self):
        t1 = np.random.randint(low=4, high=7, size=1)
        t2 = np.random.randint(low=1, high=9, size=1)
        t3 = np.random.randint(low=0, high= 240 - t1 -t2, size=1)
        b1 = np.random.choice([0, 1])
        t = np.concatenate((t1, t2, t3, b1), axis=None)
        print(t)
        return t


#generation
    def itration(self,numberitration ,min):
        w=0.9       
        c1=2.05        
        c2=2.05
        for i in range(numberitration):
            print(i,"new ineration begins with best: " ,f(self.gbest),min)
            for p in self.particles:
                r1= random.randint(0,10)
                r2= random.randint(0,10)
                nextv = w *  p.velocity + c1*r1*(abs(p.localbest-p.positions)) + c2*r2*(abs(self.gbest-p.positions))
                nextposition = p.positions + nextv
                print("next position ",nextposition)
                #update local position
                if(min):
                    if f(p.localbest) > f(nextposition):
                        p.localbest = nextposition
                        #print("local update",f(nextposition),p)
                        
                        #update global best
                        if f((self.gbest)) > f(p.localbest):
                            print(f((self.gbest)) , f(p.localbest),self.gbest)
                            self.gbest = p.localbest
                            print("best to " , f(self.gbest))
                else:
                    if f(p.localbest) < f(nextposition):
                        p.localbest = nextposition
                        print("local update",f(nextposition),p)
                        
                        #update global best
                        if f(self.gbest) < f(p.localbest):
                            self.gbest = p.localbest
                            print("best to " , f(self.gbest))
                p.positions = nextposition
                self.bestlist.append(f(self.gbest))


finalList = []
            
for i in range(10):
    
    pso = MyPSO(10)
    pso.bestlist= []
    pso.itration(30,True)
    print(f(pso.gbest))
    x = pso.bestlist[:1000]
    print("best",x)

    finalList.append(x)

print("final ",finalList)