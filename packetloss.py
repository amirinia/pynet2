
"""

The 95% confidence interval between two devices(nodes)
Based on paper "Estimating Packet Delivery Ratio for Arbitrary Packet Sizes Over Wireless Links"

It generate PDR% when you call it
if packetloss() returns false it means packet is lost and you need to resend

"""

# Packet Delivery Ratio in wireless network
PDR = 95


import random

def packetloss():
    p = random.randint(1,100)
    if(p < PDR):
        #print(p)
        return True
    else:
        return False

# f =0
# for i in range(100):
#     #print(i)
#     if packetloss() == False:
#         f+=1
# print (f)


