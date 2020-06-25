# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:21:43 2019

@author: 100730451
"""
import pandas as pd
import matplotlib.pyplot  as plt
from mpl_toolkits import mplot3d
import numpy as np

df = pd.read_csv("report/DE best .csv")
df.sort_values(by=['energy'], inplace=True)

print(df)


def convertvar(df):
    dfv = pd.DataFrame(columns=['t1','t2','t3','t4','energy','old duration' , 'lost','dead','duration'])
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
        sumduration =int(L[0])+int(L[1])+int(L[2])
        dfv = dfv.append(pd.Series([(L[0]),(L[1]),(L[2]),(L[3]),df['energy'][index],df['duration'][index],df['lost'][index],df['dead'][index],sumduration], index=dfv.columns),ignore_index=True)

    print(dfv)
    dfv.to_csv('report/1000,000.csv')

#convertvar(df)
dfv2 =pd.read_csv('report/old/DE best variables.csv')



def myplotpopulation(df):
    #df.rename({'t1': 'x', 't2': 'y'}, axis=1, inplace=True)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x= df.t1
    y= df.t2
    z= df.t3
    m = df.t4


    e = np.array(df.t4)
    c = np.ma.masked_where( (e == 1) & (e == 0), e)
    ax.scatter(x, y, z, c=c, marker='o')
    #ax.scatter(x, y, z, c=c, marker='o')
    #plt.title("Population")

    ax.set_xlabel('GTS size')
    ax.set_ylabel('CAP size')
    ax.set_zlabel('Inactive size')
    plt.show()


    

print(dfv2[-70:])

myplotpopulation(dfv2)


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def dfScatter(df):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    categories = np.unique(df.t4)
    colors = np.linspace(0, 1)
    colordict = dict(zip(categories, colors))  

    df["Color"] = df.t4.apply(lambda x: colordict[x])
    ax.scatter(df.t1, df.t2, df.t3, c=df.Color)
    plt.show()
    return fig
    ax.set_xlabel('GTS size')
    ax.set_ylabel('CAP size')
    ax.set_zlabel('Inactive size')

 
fig = dfScatter(dfv2)
#fig.savefig('fig1.png')



def myploted(df):
    x= []
    y= []

    fig = plt.figure()

    ax = fig.add_subplot()


    ax.scatter(x, y, marker='o')
    #plt.title("Pareto front")

    ax.set_xlabel('Superframe Size (s)')
    ax.set_ylabel('The Remaining Energy (mJ)')
    plt.show()

myploted(dfv2)