import time
import config
class logger:
    def __init__(self,name='log{0}-{1}-{2}-{3}.txt'.format(config.TDMA_duration,config.CSMA_duration,config.Inactive_duration,config.Multiframe_state)):
        if(config.logenabled):
            self.name = name    
            self.creat_logfile(self.name)
        else:
            pass
    
    def creat_logfile(self,name):
        if(config.logenabled):
            f = open(name,'w')
            f.write("New log is named at {0} \r\n".format(time.strftime('%X %x %Z')))
        else:
            pass

    def log(self,string):
        if(config.logenabled):
            f = open('report/log{0}-{1}-{2}-{3}.txt'.format(config.TDMA_duration,config.CSMA_duration,config.Inactive_duration,config.Multiframe_state),'a')
            f.write(time.strftime("%a, %d %b %Y %H:%M:%S")+" "+string +"\n")
            f.close()
        else:
            pass

# logg = logger()
# logg.log("salam")
# logg.log("chetori")