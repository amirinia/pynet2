# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:21:43 2019

@author: 100730451
"""
import pandas as pd
import matplotlib.pyplot  as plt
from mpl_toolkits import mplot3d
import numpy as np


filename = "DE best 2020k-100-100" #DE best 2020l-100-100
print("Convert start {}".format(filename))
df = pd.read_csv("report/{}.csv".format(filename))
df.sort_values(by=['energy'], inplace=True)

#print(df)


def convertvar(df):
    dfv = pd.DataFrame(columns=['t1','t2','t3','t4','energy','old duration' , 'lost','dead','duration'])
    for index,row in df.iterrows():
        #print(index)
        word = df['pop'][index]
        #print(word)
        #res = [int(i) for i in word.split() if i.isdigit()] 
        word = word.replace('  ', ' ')
        word = word.replace('[', '')
        word = word.replace(']', '')
        # L = ""
        L = word.split(' ')
        L = [i for i in L if i != '']
        #print(L)
        #dft['My new column'] =L[0]
        #("p",L[0],L[1],L[2],L[3])
        #dft["n"][index] =L[2]
        sumduration =int(L[0])+int(L[1])+int(L[2])
        dfv = dfv.append(pd.Series([(L[0]),(L[1]),(L[2]),(L[3]),df['energy'][index],df['duration'][index],df['lost'][index],df['dead'][index],sumduration], index=dfv.columns),ignore_index=True)

    print(dfv)
    dfv.to_csv('report/{}{}.csv'.format(filename,"report"))

convertvar(df)
dfv2 =pd.read_csv('report/{}{}.csv'.format(filename,"report"))



def myplotpopulation(df):
    #df.rename({'t1': 'x', 't2': 'y'}, axis=1, inplace=True)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x= df.t1
    y= df.t2
    z= df.t3
    e =np.array(df.energy)
    xy2 = np.ma.masked_where( (e < 6)&(e > 12000), e)
    ax.scatter(x, y, z, c=xy2, marker='o')
    ax.scatter(x, y, z, c=xy2, marker='o')
    #plt.title("Population")

    ax.set_xlabel('GTS size')
    ax.set_ylabel('CAP size')
    ax.set_zlabel('Inactive size')
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
    ax.scatter(x, y, z, c=xy2, marker='o')
    plt.title("")

    ax.set_xlabel('GTS size')
    ax.set_ylabel('CAP size')
    ax.set_zlabel('Remaining Energy (mJ)')
    plt.show()

def myplott1t2d(df):
    df.rename({'t1': 'x', 't2': 'y'}, axis=1, inplace=True)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    x= df.x
    #y= df.y
    y= df.energy
    e =np.array(df.energy)
    xy2 = np.ma.masked_where( (e < 6)&(e > 12000), e)
    ax.scatter(x, y, c=xy2, marker='o')
    plt.title("")

    ax.set_xlabel('GTS size')
    #ax.set_ylabel('CAP size')
    ax.set_ylabel('Remaining Energy (mJ)')
    plt.show()

def myplott1t2d2(df):
    df.rename({'t1': 'x', 't2': 'y'}, axis=1, inplace=True)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    #x= df.x
    x= df.y
    y= df.energy
    e =np.array(df.energy)
    xy2 = np.ma.masked_where( (e < 6)&(e > 12000), e)
    ax.scatter(x, y, c=xy2, marker='o')
    plt.title("")

    #ax.set_xlabel('GTS size')
    ax.set_xlabel('CAP size')
    ax.set_ylabel('Remaining Energy (mJ)')
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
    plt.title("Objectives")

    ax.set_xlabel('X duration(ms)')
    ax.set_ylabel('Y Lost')
    ax.set_zlabel('Z Energy(mJ)')
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
    ax.scatter(x, y, z, c=xy2, marker='o')#,s =(df.duration))
    #plt.title("Variables (sample size = superframesize)")

    ax.set_xlabel('GTS size')
    ax.set_ylabel('CAP size')
    ax.set_zlabel('inactive size')
    plt.show()

def myploted(df):
    x= df.duration
    y= df.energy
    e =np.array(df.energy)
    fig = plt.figure()

    ax = fig.add_subplot()

    xy2 = np.ma.masked_where( (e < 6)&(e > 12000), e)
    ax.scatter(x, y, c=xy2, marker='o')
    #plt.title("Pareto front")

    ax.set_xlabel('Superframe Size (ms)')
    ax.set_ylabel('The Remaining Energy (mJ)')
    plt.show()
    
lasttop =  100
print(dfv2[-lasttop:])

myplotpopulation(dfv2[-lasttop:])
myplott1t2(dfv2[-lasttop:])
myplott1t2d(dfv2[-lasttop:])
myplott1t2d2(dfv2[-lasttop:])
print("5")

myplotobj(dfv2[-lasttop:])
myplotvar(dfv2[-lasttop:])
print("7")
myploted(dfv2[-lasttop:]) # pareto
