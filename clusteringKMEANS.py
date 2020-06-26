import network
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
    def __init__(self,env, network,k=5):
        self.network = network
        self.k = k
        self.clusterheads = []
        self.clusters = []
        self.env = env
        self.action = env.process(self.run(env))


    def run(self,env): #steady pahse
        #while True:
        if self.k >16:
            print('use smaller k')
        df = pd.DataFrame(columns=['n', 'x', 'y'])
        graphi = gui.graphic(network)

        for n in self.network.nodes:
            df.loc[n] = [n.id,n.x,n.y]


        kmeans = KMeans(n_clusters=3).fit(df)
        plt.scatter(df['x'], df['y'], color='k')
        # centroids[i] = [x, y]
        centroids = {
            i+1: [np.random.randint(0, self.network.xsize), np.random.randint(0, self.network.ysize)]
            for i in range(self.k)
        }
        colmap = {1: 'r', 2: 'g', 3: 'b',4: 'y',5: 'k',6: 'm',7: 'c',8: 'pink',9 :'blue' ,10 :'green',11:'purple',12:'cyan',13:'red',14:'yellow',15:'black',16:'magenta'}
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i],s=400)


        plt.pause(1)
        plt.clf()
        plt.close()

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
        fig = plt.figure()
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k',s=400)
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])


        plt.pause(1)
        plt.clf()
        plt.close()
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
        print(3)
        df = assignment(df, centroids)

        # Plot results
        fig = plt.figure()
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k',s=400)
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])
        ax.legend()

        plt.pause(1)
        plt.clf()
        plt.close()
        print(df)

        # for i, row in df.iterrows():
            # for j, column in row.iteritems():
            # print(i,df['closest'][i])
            #print(self.network.nodes[i].id)
        

        print("nn",self.network.nodes)
        clusters = []
        for n in self.network.nodes: # add cluster to node
            if(n.id != 0):
                print(n,df['closest'][n])
                n.cluster.clear()
                n.cluster.append(df['color'][n])
                clusters.append(df['closest'][n])
        print(set(clusters))


        self.network.introduce_yourself()

        
        for c in set(clusters): # add neighbor to node
            print(c ,"is new cluster in kmean" )



                        # node.change_CulsterHead()
            mycluster1 = cluster.mycluster(c,env,self.network)
                        # mycluster1.add_node(node) # add ch to node list
            for n in self.network.nodes: # add neighbor of CH to cluster
                if(df['closest'][n] == c):
                    #print(df['closest'][n], "   ", c)

                    mycluster1.add_node(n)
                    print(n," is added")
                    #print(mycluster1.CH)
            n= random.choice(mycluster1.nodes)
            print(n," is high")
            n.change_CulsterHead()
            mycluster1.CH = n
            n.set_TDMA(len(mycluster1.nodes))
                            # # node.change_TDMA(mycluster1.TDMA_slots)
                        #self.logger.log("{0} is CH in {1} with {2} energy ++++++++++++++++++\n".format(node.id , mycluster1.id,str(node.energy) ) )
            print("{0} is CH in {1} with {2} energy ++++++++++++++++++ {3}\n".format(n.id , mycluster1.id,(n.neighbors) ,mycluster1.nodes) )
            message2 = message.Message()
            message2.broadcast(n,"node {0} is cluster Head in {1} with TDMA ".format(n.id,mycluster1.id))
                            
            self.network.add_cluster(mycluster1)
            self.clusters.append(mycluster1)
            self.network.clusterheads.append(n)
            self.clusterheads.append(n)
                        


            
        print(self.clusters)    
        print(self.clusterheads)  
        graphi = gui.graphic(self.network)  
        graphi.draw()
        print("kmeans is done")
        self.network.introduce_yourself()


        doagain = False
        print("clusters",self.network.clusters)
        for c in self.network.clusters:
                print(c,c.nodes)
                if len(c.nodes)>7:
                        print("cluster is too large")
                        doagain ==True

        if doagain:
                print("repeat Kmean")
                Kmeans(self.network,k)

        
        while True:
            closest_centroids = df['closest'].copy(deep=True)
            centroids = update(centroids)
            df = assignment(df, centroids)
            if closest_centroids.equals(df['closest']):
                break

        fig = plt.figure()
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k',s=400)
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])


        plt.pause(5)
        plt.clf()
        plt.close()
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
    # net1 = network.Net(env)
    # net1.random_net_generator(env,net1,10)
    # net1.introduce_yourself()
    # graphi = gui.graphic(net1)
    # graphi.draw_nods()

    # Kmeans(net1,3)





    #print(network.nodes[0].x)

        # def myKmeans(self,network,itrations):

            
        #     for i in range(itrations):
        #         x=random.randint(0,config.AREA_WIDTH)
        #         y=random.randint(0,config.AREA_LENGTH)
        #         nodech = node.Node(1000+i,env,2,x,y)

        #         for n in self.network.nodes:
        #             distance = 200
        #             #print(self.network.distance(n,nodech))
        #             #print(i,x,y)
        #             if(distance > self.network.distance(n,nodech)):
        #                 distance = self.network.distance(n,nodech)
        #                 print(n,nodech,distance)
        #                 n.parent.clear()
        #                 n.parent.append(nodech)
        #         print(distance)
                



    # Kmeans(network,5)
    # network.introduce_yourself()
    # graphi = gui.graphic(network)
    # graphi.draw_ch()