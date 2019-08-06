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

k = 3
env = simpy.Environment()
net1 = network.Net(env)
net1.random_net_generator(env,net1,10)
net1.introduce_yourself()
graphi = gui.graphic(net1)
graphi.draw_nods()

df = pd.DataFrame(columns=['n', 'x', 'y'])

for n in net1.nodes:
    df.loc[n] = [n.id,n.x,n.y]


kmeans = KMeans(n_clusters=3).fit(df)
plt.scatter(df['x'], df['y'], color='k')
# centroids[i] = [x, y]
centroids = {
    i+1: [np.random.randint(0, net1.xsize), np.random.randint(0, net1.ysize)]
    for i in range(k)
}
colmap = {1: 'r', 2: 'g', 3: 'b',4: 'y',5: 'k',6: 'm',7: 'c'}
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i])

plt.show()

print(df)

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
print(df.head())
fig = plt.figure()
plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k')
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i])

plt.show()
print(df)

## Update Stage
print("arrows")

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
plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k')
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i])

for i in old_centroids.keys():
    old_x = old_centroids[i][0]
    old_y = old_centroids[i][1]
    dx = (centroids[i][0] - old_centroids[i][0]) * 0.75
    dy = (centroids[i][1] - old_centroids[i][1]) * 0.75
    ax.arrow(old_x, old_y, dx, dy, head_width=2, head_length=3, fc=colmap[i], ec=colmap[i])
plt.show()
print(df)
print("done")
df = assignment(df, centroids)

# Plot results
fig = plt.figure()
plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k')
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i])

plt.show()
print(df)

# for i, row in df.iterrows():
    # for j, column in row.iteritems():
    # print(i,df['closest'][i])
    #print(net1.nodes[i].id)


for n in net1.nodes:
    if(n.id != 0):
        print(n,df['closest'][n])
        n.parent_setter(df['color'][n])

net1.introduce_yourself()

graphi.Kmeans_draw()


# while True:
#     closest_centroids = df['closest'].copy(deep=True)
#     centroids = update(centroids)
#     df = assignment(df, centroids)
#     if closest_centroids.equals(df['closest']):
#         break

# fig = plt.figure(figsize=(5, 5))
# plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k')
# for i in centroids.keys():
#     plt.scatter(*centroids[i], color=colmap[i])

# plt.show()

# print(df)

# centroids = kmeans.cluster_centers_

# fig = plt.figure(figsize=(5, 5))



# plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k')
# for idx, centroid in enumerate(centroids):
#     plt.scatter(*centroid, color=colmap[idx+1])

# plt.show()














#print(net1.nodes[0].x)

def Kmeans(network,itrations):

    
    for i in range(itrations):
        x=random.randint(0,config.AREA_WIDTH)
        y=random.randint(0,config.AREA_LENGTH)
        nodech = node.Node(1000+i,env,2,x,y)

        for n in net1.nodes:
            distance = 200
            #print(net1.distance(n,nodech))
            #print(i,x,y)
            if(distance > net1.distance(n,nodech)):
                distance = net1.distance(n,nodech)
                print(n,nodech,distance)
                n.parent.clear()
                n.parent.append(nodech)
        print(distance)
        



# Kmeans(net1,5)
# net1.introduce_yourself()
# graphi = gui.graphic(net1)
# graphi.draw_ch()