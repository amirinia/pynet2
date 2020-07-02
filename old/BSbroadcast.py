#at begining you can set parameters in config file
import gui
import simpy
import ieee802154
import node

# to run simulation you need initial ieee802154s ( just simply define nodes and addd to ieee802154 or use random generator)
env = simpy.Environment()
net1 = ieee802154.Net(env)
net1.random_net_generator(env,net1,30)
net1.introduce_yourself()
graphi = gui.graphic(net1)
graphi.draw_nods()
graphi.draw_neighbors()


print("++++++++++++++++++++++++++++++++++++++++++ run begin ++++++++++++++++++++++++")
env.run(until=140)#config.MAX_RUNTIME)
print("++++++++++++++++++++++++++++++++++++++++++ run end ++++++++++++++++++++++++")

net1.ieee802154_packet_summery()

for n in net1.nodes:
    print(n,n.is_CH,n.distance)
graphi.draw_neighbors()
# net1.ieee802154_outboxes()
# net1.ieee802154_inboxes()