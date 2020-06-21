import config as setting

class Superframe():
    def __init__(self,TDMA_slot = setting.TDMA_duration,CSMA_slot = setting.CSMA_duration,Inactive_slot = setting.Inactive_duration):
        self.TDMA_slot = TDMA_slot
        self.CSMA_slot = CSMA_slot
        self.Inactive_slot = Inactive_slot
        self.Multi = False
    
    def __str__(self):
        return str("superframe {0} {1} {2} ".format(self.TDMA_slot ,self.CSMA_slot,self.Inactive_slot))

    def __repr__(self):
        return str("superframe {0} {1} {2} ".format(self.TDMA_slot ,self.CSMA_slot,self.Inactive_slot))


# s1 = Superframe(2,3,4)
# print(s1)