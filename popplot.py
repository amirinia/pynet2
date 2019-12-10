# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:21:43 2019

@author: 100730451
"""
import pandas as pd
import matplotlib.pyplot  as plt
from mpl_toolkits import mplot3d
import numpy as np

df = pd.read_csv("DE best .csv")
df.sort_values(by=['energy'], inplace=True)

#print(df)

dfv2 =pd.read_csv('report/DE best variables.csv')

def convertvar(df):
    dfv = pd.DataFrame(columns=['t1','t2','t3','t4','energy','duration' , 'lost','dead'])
    for index,row in df.iterrows():
        print(index)
        word = df['pop'][index]
        print(word)
        #res = [int(i) for i in word.split() if i.isdigit()] 
        word = word.replace('  ', ' ')
        word = word.replace('[', '')
        word = word.replace(']', '')
        # L = ""
        L = word.split(' ')
        L = [i for i in L if i != '']
        print(L)
        #dft['My new column'] =L[0]
        #("p",L[0],L[1],L[2],L[3])
        #dft["n"][index] =L[2]
        dfv = dfv.append(pd.Series([(L[0]),(L[1]),(L[2]),(L[3]),df['energy'][index],df['duration'][index],df['lost'][index],df['dead'][index]], index=dfv.columns),ignore_index=True)

    print(dfv)
    dfv.to_csv('report/DE best variables.csv')

def myplotpopulation(df):
    #df.rename({'t1': 'x', 't2': 'y'}, axis=1, inplace=True)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x= df.t1
    y= df.t2
    z= df.t3
    e =np.array(df.energy)
    xy2 = np.ma.masked_where( (e < 6)&(e > 12000), e)
    ax.scatter(x, y, z, c=xy2, marker='o',s =(df.duration))
    plt.title("population")

    ax.set_xlabel('X t1')
    ax.set_ylabel('Y t2')
    ax.set_zlabel('Z t3')
    plt.show()

def myplott1t2(df):
    df.rename({'t1': 'x', 't2': 'y'}, axis=1, inplace=True)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x= df.x
    y= df.y
    z= df.energy
    e =np.array(df.energy)
    xy2 = np.ma.masked_where( (e < 6)&(e > 12000), e)
    ax.scatter(x, y, z, c=xy2, marker='o',s =(df.duration))
    plt.title("t1 t2")

    ax.set_xlabel('X t1')
    ax.set_ylabel('Y t2')
    ax.set_zlabel('Z Energy')
    plt.show()
    
def myplotobj(df):
    df.rename({'duration': 'x', 'lost': 'y'}, axis=1, inplace=True)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x= df.x
    y= df.y
    z= df.energy
    e =np.array(df.energy)
    xy2 = np.ma.masked_where( (e < 6)&(e > 12000), e)
    ax.scatter(x, y, z, c=xy2, marker='o',s =(df.energy/1000))
    plt.title("objective")

    ax.set_xlabel('X duration')
    ax.set_ylabel('Y Lost')
    ax.set_zlabel('Z Energy')
    plt.show()

def myplotvar(df):
    df.rename({'t1': 'x', 't2': 'y'}, axis=1, inplace=True)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x= df.x
    y= df.y
    z= df.t3
    e =np.array(df.energy)
    xy2 = np.ma.masked_where( (e < 6)&(e > 12000), e)
    ax.scatter(x, y, z, c=xy2, marker='o',s =(df.t3))
    plt.title("Variables")

    ax.set_xlabel('X t1')
    ax.set_ylabel('Y t2')
    ax.set_zlabel('Z t3')
    plt.show()

def myploted(df):
    x= df.duration
    y= df.energy
    e =np.array(df.energy)
    fig = plt.figure()

    ax = fig.add_subplot()

    xy2 = np.ma.masked_where( (e < 6)&(e > 12000), e)
    ax.scatter(x, y, c=xy2, marker='o',s =(df.duration))

    ax.set_xlabel('<== Delay Min')
    ax.set_ylabel('Energy Max ==>')
    plt.title("Pareto front")
    plt.show()
    

print(dfv2[-100:])

myplotpopulation(dfv2)
myplott1t2(dfv2[-200:])

myplotobj(dfv2[-200:])
myplotvar(dfv2[-200:])
myploted(dfv2[-300:])