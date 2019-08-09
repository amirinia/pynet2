import network
import node
import simpy
import cluster

class simulation:
    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())