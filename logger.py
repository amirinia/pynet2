import time
import config
class logger:
    def __init__(self,name='log{0}-{1}-{2}-{3}.txt'.format(config.TDMA_duration,config.CSMA_duration,config.Inactive_duration,config.Multiframe_state)):
        #self.name = name    
        #self.creat_logfile(self.name)
        pass
    
    def creat_logfile(self,name):
        #f = open(name,'w')
        #f.write("New log is named at {0} \r\n".format(time.strftime('%X %x %Z')))
        pass

    def log(self,string):
        #f = open('report/log{0}-{1}-{2}-{3}.txt'.format(config.TDMA_duration,config.CSMA_duration,config.Inactive_duration,config.Multiframe_state),'a')
        #f.write(time.strftime("%a, %d %b %Y %H:%M:%S")+" "+string +"\n")
        #f.close()
        pass

# logg = logger()
# logg.log("salam")
# logg.log("chetori")