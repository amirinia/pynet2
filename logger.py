import time
class logger:
    def __init__(self,name='log'):
        self.name = name    
        self.creat_logfile(self.name)

    def creat_logfile(self,name):
        f = open(name,'w')
        f.write("New log is named at {0} \r\n".format(time.strftime('%X %x %Z')))

    def log(self,string):
        f = open('log','a')
        f.write(string +"\n")
        f.close()

# logg = logger()
# logg.log("salam")
# logg.log("chetori")