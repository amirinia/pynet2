import matplotlib.pyplot as plt 
import pandas as pd 





#print(df1.id,df1.lost)
def plotpacket():
    df1 = pd.read_csv('report/packet.csv')
    df = df1[1:21]
    ax = plt.gca()
    df.plot(kind='line',x='id',y='sent',color='red',ax = ax)
    df.plot(kind='line',x='id',y='received', color='blue', ax=ax)
    plt.savefig('report/packet{0} {1} .png'.format(1,1))

    #df.plot(kind='bar',x='id',y='lost')
    #plt.savefig('report/packet{0} {1} .png'.format(1,2))
    plt.pause(15)
    plt.clf()
    plt.close()

#print(df2)
def plotenergy():
    df2 = pd.read_csv('report/introduce_yourself.csv')

    df2.plot(kind='bar',x='id',y='energy')
    plt.savefig('report/energy{0} {1} .png'.format(1,2))
    plt.pause(50)
    plt.clf()
    plt.close()


#plotpacket()
#plotenergy()