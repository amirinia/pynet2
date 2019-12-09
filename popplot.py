# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:21:43 2019

@author: 100730451
"""
import pandas as pd
import matplotlib.pyplot  as plt
df = pd.read_csv("DE best .csv")
dfs = df.sort_values(by=['energy'], inplace=True)
print(df[-10:])
dft = df[-2000:]
print(dft['pop'])


def myplot(df):
    df.rename({'duration': 'x', 'lost': 'y'}, axis=1, inplace=True)
    #df2.rename({'0': 'x', '1': 'y'}, axis=1, inplace=True)
    #df3.rename({'0': 'x', '1': 'y'}, axis=1, inplace=True)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x= df.x
    y= df.y
    z=df.energy
    ax.scatter(x, y, z, c='c', marker='o',s =(df.energy/1000))
    #x2= df2.x
    #y2= df2.y
    #z2=f(df2.x,df2.y)
    #ax.scatter(x2, y2, z2, c='b', marker='+')
    #x3= df3.x
    #y3= df3.y
    #z3=f(df3.x,df3.y)
    #ax.scatter(x3, y3, z3, c='r', marker='o')
    ax.set_xlabel('X Size')
    ax.set_ylabel('Y Lost')
    ax.set_zlabel('Z Energy')
    plt.show()
   
myplot(dft)