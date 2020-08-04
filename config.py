import math

## Runtime configuration
MAX_RUNTIME = 2000
#ALERT TIME
ALERT_TIME = 1000
ALERT_END = 4000

# area definition
AREA_WIDTH = 300
AREA_LENGTH = 300
xsize = AREA_WIDTH
ysize = AREA_LENGTH

#Superframe
CSMA_duration = 9
TDMA_duration = 7
Inactive_duration = 16

Duration = CSMA_duration + TDMA_duration + Inactive_duration

# print
printenabled = False

#gui config
guienabled = False
guiduration = 5

#Log
logenabled = False

#save excel
excelsave = False

# and config
BEACONING_TIME       = 5
Base_Sattion_Beaconning_period = 5 #per superframe
cluster_rotation_period = 5

# alert position
alertx = 270
alerty = 110
Alert_RANGE = 90 # meters
Alert_increase_temp = 300

# propagation {0: "Free space", 1: "two-ray ground", 2: "Shadowing"}
propagation_type = 0

#aggregate time
AGGREGATE_TIME = 10

# node sensor range
COVERAGE_RADIUS = 15 # meters 

#ENERGY
# initial energy at every node's battery
INITIAL_ENERGY = 2000 # mili Joules 2000

P_TX = 0.084  * 100 # Watts to transmite 
P_RX = 0.073  * 100 # Watts to receive

#dead node threshold
DEAD_NODE_THRESHOLD = 100.299
LOW_NODE_THRESHOLD = 300.5

# node transmission energy cnsumption
PACKET_ENERGY_CONSUMPTION       = -0.00005 #* 1000000
NODE_SLEEP_ENERGY_CONSUMPTION   = -0.00001 #* 1000000
NODE_RUNING_ENERGY_CONSUMPTION  = -0.00002 #* 1000000

#node CPU
NODE_AGGREGATE_ENERGY_CONSUMPTION = -0.00002

# node transmission range node discovery
TX_RANGE = 70 # meters 30
BSID = -1

# controller  position
BS_POS_X = 0.0
BS_POS_Y = 0.0

# packet configs
MSG_LENGTH = 4000 # bits
HEADER_LENGTH = 150 # bits

# multiframe 
Multiframe_size = 2
Multiframe_state = False


RESULTS_PATH = 'report/'


