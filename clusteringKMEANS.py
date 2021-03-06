import ieee802154
import simpy
import random
import config
import node
import gui
import sklearn
import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cluster
import simpy
import message

class Kmeans:
    def __init__(self,env, ieee802154,k=5):
        self.ieee802154 = ieee802154
        self.k = k
        self.clusterheads = []
        self.clusters = []
        self.notclustered = []
        self.env = env
        self.action = env.process(self.run(env))


    def run(self,env): #steady pahse
        #while True:
        if self.k >16:
            if config.printenabled:
                print('use smaller k')
        df = pd.DataFrame(columns=['n', 'x', 'y'])
        if(config.guienabled):
            graphi = gui.graphic(ieee802154)

        for n in self.ieee802154.nodes:
            df.loc[n] = [n.id,n.x,n.y]


        kmeans = KMeans(n_clusters=3).fit(df)
        plt.scatter(df['x'], df['y'], color='k')
            # centroids[i] = [x, y]
        centroids = {
                i+1: [np.random.randint(0, config.xsize), np.random.randint(0, config.ysize)]
                for i in range(self.k)
            }
        colmap = {1: 'r', 2: 'g', 3: 'b',4: 'y',5: 'k',6: 'm',7: 'c',8: 'pink',9 :'blue' ,10 :'green',11:'purple',12:'cyan',13:'red',14:'yellow',15:'black',16:'magenta'}
        
        if(config.guienabled):
            for i in centroids.keys():
                plt.scatter(*centroids[i], color=colmap[i],s=400)


            plt.pause(1)
            plt.clf()
            plt.close()

        if config.printenabled:
            print(1)

        def assignment(df, centroids):
            for i in centroids.keys():
                # sqrt((x1 - x2)^2 - (y1 - y2)^2)
                df['distance_from_{}'.format(i)] = (
                    np.sqrt(
                        (df['x'] - centroids[i][0]) ** 2
                        + (df['y'] - centroids[i][1]) ** 2
                    )
                )
            centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
            df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
            df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
            df['color'] = df['closest'].map(lambda x: colmap[x])
            return df

        df = assignment(df, centroids)
        # print(df.head())
        if(config.guienabled):

            fig = plt.figure()
            plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k',s=400)
            for i in centroids.keys():
                plt.scatter(*centroids[i], color=colmap[i])


            plt.pause(1)
            plt.clf()
            plt.close()
        if config.printenabled:
            print(2)

        ## Update Stage
        # print("arrows")

        import copy

        old_centroids = copy.deepcopy(centroids)

        def update(k):
            for i in centroids.keys():
                centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
                centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
            return k

        centroids = update(centroids)
        
        if(config.guienabled):
            fig = plt.figure()
            ax = plt.axes()
            plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k',s=400)
            for i in centroids.keys():
                plt.scatter(*centroids[i], color=colmap[i])

            for i in old_centroids.keys():
                old_x = old_centroids[i][0]
                old_y = old_centroids[i][1]
                dx = (centroids[i][0] - old_centroids[i][0]) * 0.75
                dy = (centroids[i][1] - old_centroids[i][1]) * 0.75
                ax.arrow(old_x, old_y, dx, dy, head_width=2, head_length=3, fc=colmap[i], ec=colmap[i])

            plt.pause(1)
            plt.clf()
            plt.close()
        if config.printenabled:
            print(3)
        df = assignment(df, centroids)

        # Plot results
        if(config.guienabled):
            fig = plt.figure()
            plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k',s=400)
            for i in centroids.keys():
                plt.scatter(*centroids[i], color=colmap[i])
            ax.legend()

            plt.pause(1)
            plt.clf()
            plt.close()
        if config.printenabled:

            print(df)

        # for i, row in df.iterrows():
            # for j, column in row.iteritems():
            # print(i,df['closest'][i])
            #print(self.ieee802154.nodes[i].id)
        


        doagain = False
        if config.printenabled:
            print("clusters",self.ieee802154.clusters)
        for c in self.ieee802154.clusters:
                print(c,c.nodes)
                if (len(c.nodes)>7 or len(c.nodes)<2 ):
                        if config.printenabled:
                            print("cluster is too large")
                        doagain ==True

        if doagain:
                if config.printenabled:
                    print("repeat Kmean")
                Kmeans(self.env,self.ieee802154,self.k)

        
        while True:
            closest_centroids = df['closest'].copy(deep=True)
            centroids = update(centroids)
            df = assignment(df, centroids)
            if closest_centroids.equals(df['closest']):
                break
        
        if(config.guienabled):
            fig = plt.figure()
            plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k',s=400)
            for i in centroids.keys():
                plt.scatter(*centroids[i], color=colmap[i])


            plt.pause(5)
            plt.clf()
            plt.close()



        if config.printenabled:
            print("nn",self.ieee802154.nodes)
        clusters = []
        for n in self.ieee802154.nodes: # add cluster to node
            if(n.id != 0):
                #print(n,df['color'][n])
                n.cluster.clear()
                n.cluster.append(df['closest'][n])
                clusters.append(df['closest'][n])
        if config.printenabled:
            print("clusss ",set(clusters))



        
        for c in set(clusters): # add neighbor to node
            if config.printenabled:
                print(c ,"is new cluster in kmean" )
                        # node.change_CulsterHead()
            mycluster1 = cluster.mycluster(c,env,self.ieee802154)
                        # mycluster1.add_node(node) # add ch to node list
            for n in self.ieee802154.nodes: # add neighbor of CH to cluster
                if(df['closest'][n] == c and n.id != 0):
                    #print(df['closest'][n], "   ", c)
                    mycluster1.add_node(n)
                    if config.printenabled:
                        print(n," is added")
            if config.printenabled:
                print("c nodws",mycluster1.nodes)
            if(len(mycluster1.nodes) >7):
                doagain == True
            n= random.choice(mycluster1.nodes)
            # for n in self.clusterheads:
            #     for nei in n.neighbors:
            #         if n == nei:
            #             n= random.choice(mycluster1.nodes)

            #print(n," is high")
            if( n.id != 0 and n not in self.clusterheads):
                n.change_CulsterHead()
                mycluster1.CH = n
                n.set_TDMA(len(mycluster1.nodes))
                                # # node.change_TDMA(mycluster1.TDMA_slots)
                            #self.logger.log("{0} is CH in {1} with {2} energy ++++++++++++++++++\n".format(node.id , mycluster1.id,str(node.energy) ) )
                if config.printenabled:
                    print("{0} is CH in {1} with {2} energy ++++++++++++++++++ {3}\n".format(n.id , mycluster1.id,(n.neighbors) ,mycluster1.nodes) )
                message2 = message.Message()
                message2.broadcast(n,"node {0} is cluster Head in {1} with TDMA ".format(n.id,mycluster1.id),mycluster1.nodes)
                                
                self.ieee802154.add_cluster(mycluster1)
                self.clusters.append(mycluster1)
                self.ieee802154.clusterheads.append(n)
                self.clusterheads.append(n)
                        

        if config.printenabled:
            print("nodes ",self.ieee802154.nodes) 
            print("clusters ",self.clusters)    
            print("CHs ",self.clusterheads)  

            print("kmeans is done")

        for node in self.ieee802154.nodes:
            #print(node.id, node.is_CH)
            if (node.is_CH == False):
                if (len(node.parent) == 0):
                    self.notclustered.append(node)

        if(len(self.notclustered) != 0):
            if config.printenabled:
                print("these are not clustered area ",self.notclustered)
        
        for c in self.clusters:
            for node in c.nodes:
                if(node.energy >= max(neighbor.energy for neighbor in c.nodes)):

                    c.cluster_head_setter(node)
                    c.CH = node
                    node.change_CulsterHead()
                    node.is_CH = True
                    #self.logger.log("{0} is CH in cluster {1} with {2}  ++++++++++++++++++ area\n".format(node.id , c.id,str(c.nodes) ) )
                    if config.printenabled:
                        print("{0} is CH in cluster {1} with {2}  ++++++++++++++++++ is CH {3} area \n".format(node.id , c.id,str(c.nodes),node.is_CH ) )
                    message2 = message.Message()
                    message2.broadcast(node,"node {0} is cluster Head in {1} with TDMA ".format(node.id,c.id),node.neighbors)
                    self.ieee802154.clusterheads.append(node)
                    self.clusterheads.append(node)
            self.ieee802154.add_cluster(c)

        self.ieee802154.introduce_yourself()
        if(config.guienabled):

            graphi = gui.graphic(self.ieee802154)  
            graphi.draw()


        yield self.env.timeout(1)

        # labels = kmeans.predict(df)
        # centroids = kmeans.cluster_centers_

        # fig = plt.figure()

        # colors = map(lambda x: colmap[x+1], labels)

        # plt.scatter(df['x'], df['y'], color=colors, alpha=0.5, edgecolor='k',s=400)
        # for idx, centroid in enumerate(centroids):
        #     plt.scatter(*centroid, color=colmap[idx+1])

        # plt.show()

        
        # print(df)

        # centroids = kmeans.cluster_centers_

        # fig = plt.figure(figsize=(5, 5))



        # plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k')
        # for idx, centroid in enumerate(centroids):
        #     plt.scatter(*centroid, color=colmap[idx+1])

        # plt.show()
        



    # env = simpy.Environment()
    # net1 = ieee802154.Net(env)
    # net1.random_net_generator(env,net1,10)
    # net1.introduce_yourself()
    # graphi = gui.graphic(net1)
    # graphi.draw_nods()

    # Kmeans(net1,3)





    #print(ieee802154.nodes[0].x)

        # def myKmeans(self,ieee802154,itrations):

            
        #     for i in range(itrations):
        #         x=random.randint(0,config.AREA_WIDTH)
        #         y=random.randint(0,config.AREA_LENGTH)
        #         nodech = node.Node(1000+i,env,2,x,y)

        #         for n in self.ieee802154.nodes:
        #             distance = 200
        #             #print(self.ieee802154.distance(n,nodech))
        #             #print(i,x,y)
        #             if(distance > self.ieee802154.distance(n,nodech)):
        #                 distance = self.ieee802154.distance(n,nodech)
        #                 print(n,nodech,distance)
        #                 n.parent.clear()
        #                 n.parent.append(nodech)
        #         print(distance)
                



    # Kmeans(ieee802154,5)
    # ieee802154.introduce_yourself()
    # graphi = gui.graphic(ieee802154)
    # graphi.draw_ch()