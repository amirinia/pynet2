import networkx as nx
import matplotlib.pyplot as plt
import ieee802154
import matplotlib.animation as animation
import time 
import config
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook


class graphic:
    def __init__(self, myieee802154):
        self.myieee802154 = myieee802154

  
    def draw(self):
        print("draw \n")
        #self.myieee802154.introduce_yourself()
        G = nx.Graph()
        G.add_node(0,pos=(config.xsize/2,config.ysize/2))
        for node in self.myieee802154.nodes:
            if(node.is_alive == True):
                # print("for node in self.myieee802154.nodes {0} and cluster head {1}".format(node,node.parent))

                G.add_node(node.id,pos=(node.x,node.y))
                
                if(node.is_CH == True): # if there is no parrent
                    if(node.is_alive==True):
                        G.add_edge(0,node.id)
                # if(len(node.parent)!=0):
                #     if(node.parent[0].is_alive==True):
                #         G.add_edge(0,node.parent[0].id)
                if(len(node.parent)!=0):
                    if(node.parent[0].is_alive==True):
                        G.add_edge(node.id,node.parent[0].id)
            else: # deadposition
                G.add_node(node.id,pos=(node.x,node.y))

        nodelistCH = []
        deadlist = []
        for node in self.myieee802154.nodes:
            if(node.is_alive == True):
                if(node.is_CH == True):
                   # print(node.id," is CH on draw",)
                    nodelistCH.append(node.id)
            else:
                deadlist.append(node.id)
                print(node.id," id dead in gui")
        
        #print(deadlist)

        nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=400)
        #ani = animation.FuncAnimation(fig, animate, interval=1000)
        nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=[0], node_size=1000, node_color='#66ff66')
        nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=nodelistCH, node_size=700, node_color='#ff80ff')
        nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=deadlist, node_size=500, node_color='#ff0000')

        mng = plt.get_current_fig_manager()
        #mng.full_screen_toggle()
        mng.set_window_title("draw")

        plt.pause(config.guiduration)
        plt.clf()
        plt.close()
        # plt.show()

        

    def drawdead(self,title):
        print("draw dead\n")
        G = nx.Graph()
        G.add_node(0,pos=(config.xsize/2,config.ysize/2))
        for node in self.myieee802154.nodes:
            if(node.is_alive == True):
                # print("for node in self.myieee802154.nodes {0} and cluster head {1}".format(node,node.parent))

                G.add_node(node.id,pos=(node.x,node.y))
                
                if(len(node.parent)!=0):
                    if(node.parent[0].is_alive==True):
                        G.add_edge(0,node.parent[0].id)
                if(len(node.parent)!=0):
                    if(node.parent[0].is_alive==True):
                        G.add_edge(node.id,node.parent[0].id)

        nodelistCH = []
        for node in self.myieee802154.nodes:
            if(node.is_alive == True):
                if(node.is_CH == True):
                    nodelistCH.append(node.id)
        # print(nodelistCH)
        nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=400)
        #ani = animation.FuncAnimation(fig, animate, interval=1000)
        nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=[0], node_size=1000, node_color='#66ff66')
        nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=nodelistCH, node_size=700, node_color='#ff80ff')
        mng = plt.get_current_fig_manager()
        #mng.full_screen_toggle()
        mng.set_window_title("dead node {0}".format(title))

        plt.title("dead mode")

        plt.pause(config.guiduration)
        plt.clf()
        plt.close()



    def draw_clusters(self):
        print("GUI CLUSTERS")

        G = nx.Graph()
        for node in self.myieee802154.nodes:
            if(node.is_alive == True):
                G.add_node(node.id,pos=(node.x,node.y))
                #G.add_edge(node,"BS")
        # nodes in cluster
        for node in self.myieee802154.nodes:
            if(node.is_alive==True):
                if(len(node.parent)!=0):
                    
                    print("netwww ",node,node.x,node.y)
                    G.add_edge(node.id,node.parent[0].id)
                    
        for cluster in self.myieee802154.clusters:
            #if(cluster.is_alive==True):
                print("gui cluster",cluster)
                for node in cluster.nodes:
                    print(node,node.x,node.y,node.parent[0],node.parent[0].x,node.parent[0].y)
                    if(node.is_alive == True):
                        if(len(node.parent)!=0):
                            #G.add_edge(node,node.parent)
                            #print("({0}, {1})".format(type(node),type(node.parent[0])))
                            #print("({0}, {1})".format((node),(node.parent[0])))
                            G.add_edge(node.id,next(reversed(node.parent)))
        nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=400)
        if self.myieee802154.alert :
                G.add_node("Fire",pos=(config.alertx,config.alerty))
                nx.draw_ieee802154x(G, nx.get_node_attributes(G, 'pos'), nodelist=["Fire"], node_size=1000, node_color='#FF0000')
        #ani = animation.FuncAnimation(fig, animate, interval=1000)
        if not self.myieee802154.alert:
            G.add_node("Solve",pos=(config.alertx,config.alerty))
            nx.draw_ieee802154x(G, nx.get_node_attributes(G, 'pos'), nodelist=["Solve"], node_size=2000, node_color='#00ff80')
        #ani = animation.FuncAnimation(fig, animate, interval=1000)

        plt.legend("ieee802154")

        plt.show()


    def draw_neighbors(self):
            print("GUI NEIGHBORS TABLE")

            G = nx.Graph()

            for node in self.myieee802154.nodes:
                if(node.is_alive == True):
                    G.add_node(node.id,pos=(node.x,node.y,))
                #G.add_edge(node,"BS")

                #print("draw node",node)

            for node in self.myieee802154.nodes:
                if(node.is_alive==True):
                    #print("draw edge",node)
                    for neighbor in node.neighbors:
                        if(neighbor.is_alive == True):
                            #print("{0} nei {1}".format(node,neighbor))
                            G.add_edge(node.id,neighbor.id)
            nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True)
            #ani = animation.FuncAnimation(fig, animate, interval=1000)
            plt.legend("ieee802154")
            plt.show()


    def draw_nods(self):
            print("GUI NODES ONLY")
            G = nx.Graph()
            for node in self.myieee802154.nodes:
                if(node.is_alive == True):
                    G.add_node(node.id,pos=(node.x,node.y),weight=node.id)
                    #print("draw ",node.x,node.y)
                    #G.add_edge(node.id,0,weight=node.id)
                #print(node)
            pos = nx.get_node_attributes(G, 'pos')
            nx.draw(G, pos, with_labels=True)
            #ani = animation.FuncAnimation(fig, animate, interval=1000)
            edge_labels = { (u,v): d['weight'] for u,v,d in G.edges(data=True) }
            nx.draw_networkx_nodes(G,pos,node_size=400)
            nx.draw_networkx_edges(G,pos)
            nx.draw_networkx_labels(G,pos,)
            nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
            nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=[0], node_size=1000, node_color='#66ff66')

            plt.title("Graph Title")
            plt.pause(config.guiduration)
            plt.clf()
            plt.close()

    def draw_ch(self):
            print("GUI NODES CH ONLY")
            G = nx.Graph()
            for node in self.myieee802154.nodes:
                if(node.is_alive == True):
                    G.add_node(node.id,pos=(node.x,node.y),weight=node.id)


            for node in self.myieee802154.nodes:
                if(node.is_alive == True):
                    for node1 in self.myieee802154.nodes:
                        if node is not node1:
                            #print("bbbb",node.parent[0],node,node1.parent[0],node1,str(node.parent[0])==str(node1.parent[0]))

                            if (str(node.parent[0])==str(node1.parent[0])):
                                print("jjjj",node,node1)
                                G.add_edge(node.id,node1.id)



            nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True)
            #ani = animation.FuncAnimation(fig, animate, interval=1000)
            plt.legend("ieee802154")
            plt.show()

    def Kmeans_draw(self):
        print("GUI Kmean ONLY")
        G = nx.Graph()
        for node in self.myieee802154.nodes:
            if(node.is_alive == True):
                G.add_node(node.id,pos=(node.x,node.y),weight=node.id)


        for node in self.myieee802154.nodes:
            if(node.id != 0):
                if(node.is_alive == True):
                    for node1 in self.myieee802154.nodes:
                        if(node1.id != 0):
                            if node is not node1:
                                #print("bbbb",node.parent[0],node,node1.parent[0],node1,str(node.parent[0])==str(node1.parent[0]))

                                if (str(node.cluster[0])==str(node1.cluster[0])):
                                    #print("Kmean",node,node1)
                                    G.add_edge(node.id,node1.id)
        nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True)
        #ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.legend("ieee802154")

        plt.pause(config.guiduration)
        plt.clf()
        plt.close()


    def alert(self):

        G = nx.Graph()
        G.add_node(0,pos=(config.xsize/2,config.ysize/2))
        for node in self.myieee802154.nodes:
            if(node.is_alive == True):
                # print("for node in self.myieee802154.nodes {0} and cluster head {1}".format(node,node.parent))

                G.add_node(node.id,pos=(node.x,node.y))
                
                if(len(node.parent)!=0):
                    if(node.parent[0].is_alive==True):
                        G.add_edge(0,node.parent[0].id)
                if(len(node.parent)!=0):
                    if(node.parent[0].is_alive==True):
                        G.add_edge(node.id,node.parent[0].id)


        nodelistCH = []
        for node in self.myieee802154.nodes:
            if(node.is_alive == True):
                if(node.is_CH == True):
                    nodelistCH.append(node.id)

        G.add_node("Fire",pos=(config.alertx,config.alerty))
        nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=400)
        nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=["Fire"], node_size=1300, node_color='#FF0000')
        nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=[0], node_size=1000, node_color='#66ff66')
        nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=nodelistCH, node_size=700, node_color='#ff80ff')
        mng = plt.get_current_fig_manager()
        #mng.full_screen_toggle()
        mng.set_window_title("Fire happens")
        plt.title("alert")

        plt.pause(config.guiduration)
        plt.clf()
        plt.close()


    def alert_sloved(self):
        G = nx.Graph()
        G.add_node(0,pos=(config.xsize/2,config.ysize/2))
        for node in self.myieee802154.nodes:
            if(node.is_alive == True):
                # print("for node in self.myieee802154.nodes {0} and cluster head {1}".format(node,node.parent))

                G.add_node(node.id,pos=(node.x,node.y))
                
                if(len(node.parent)!=0):
                    if(node.parent[0].is_alive==True):
                        G.add_edge(0,node.parent[0].id)
                if(len(node.parent)!=0):
                    if(node.parent[0].is_alive==True):
                        G.add_edge(node.id,node.parent[0].id)


        nodelistCH = []
        for node in self.myieee802154.nodes:
            if(node.is_alive == True):
                if(node.is_CH == True):
                    nodelistCH.append(node.id)

        G.add_node("Solved",pos=(config.alertx,config.alerty))
        nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=400)
        nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=["Solved"], node_size=2200, node_color='#24D39A')
        nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=[0], node_size=3000, node_color='#66ff66')
        nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), nodelist=nodelistCH, node_size=700, node_color='#ff80ff')
        mng = plt.get_current_fig_manager()
        #mng.full_screen_toggle()
        mng.set_window_title("Fire happens")
        plt.pause(config.guiduration)
        plt.clf()

        plt.close()
