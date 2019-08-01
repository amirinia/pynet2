"""
RSSI (received signal strength indicator)
Measured Power = -69 (for kontakt BLE beacons)
N (Constant depends on the Environmental factor. Range 2-4)
Distance = 10 ^ ((Measured Power – RSSI)/(10 * N))

RSSI = -60, -69, -80

N = 2

Distance for RSSI -60 = 10 ^ ((-69 – (-60))/(10 * 2))
= 0.35 meter

2. Distance for RSSI -69 = 10 ^ ((-69 – (-69))/(10 * 2))

= 1 meter

3. Distance for RSSI -80 = 10 ^ ((-69 – (-80))/(10 * 2))

= 3.54 meter


Acceptable Signal Strengths
Signal Strength	TL;DR	 	Required for
-30 dBm	Amazing	Max achievable signal strength. The client can only be a few feet from the AP to achieve this. Not typical or desirable in the real world.	N/A
-67 dBm	Very Good	Minimum signal strength for applications that require very reliable, timely delivery of data packets.	VoIP/VoWiFi, streaming video
-70 dBm	Okay	Minimum signal strength for reliable packet delivery.	Email, web
-80 dBm	Not Good	Minimum signal strength for basic connectivity. Packet delivery may be unreliable.	N/A
-90 dBm	Unusable

"""

import math

def RSSI(distance, n = 2, Measured_Power = -69):
    RSSI_value =  - (10 * n *  math.log10(distance)) + Measured_Power
    return RSSI_value

def RSSI_nodes(node1, node2, n = 2, Measured_Power = -69):
    distance = math.sqrt(((node1.x-node2.x)**2)+((node1.y-node2.y)**2))
    RSSI_value =  - (10 * n *  math.log10(distance)) + Measured_Power
    return RSSI_value
    

# print(RSSI(0.35))
# print(RSSI(1))
# print(RSSI(3.54))
# print(RSSI(100))
