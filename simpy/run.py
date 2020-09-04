import simpy






class Car(object):
     def __init__(self, env):
         self.env = env
         # Start the run process everytime an instance is created.
         self.action = env.process(self.run())
         self.initial = False

     def run(self):
         while True:

             if(not self.initial):
                print('Start parking and charging at %d' % self.env.now)
                charge_duration = 5
             # We yield the process that process() returns
             # to wait for it to finish
                yield self.env.process(self.charge(charge_duration))
                self.initial = True


             # The charge process has finished and
             # we can start driving again.
             print('Start driving at %d' % self.env.now)
             trip_duration = 2
             yield self.env.timeout(trip_duration)

     def charge(self, duration):
         print("daram charge misham")
         yield self.env.timeout(duration)


import simpy
env = simpy.Environment()
car = Car(env)
env.run(until=15)
