import math
# area definition
AREA_WIDTH = 300
AREA_LENGTH = 200

#TDMA
CSMA_duration = 9
TDMA_duration = 8
Inactive_duration = 14

Duration = CSMA_duration + TDMA_duration + Inactive_duration

# and config
BEACONING_TIME       = 5
Base_Sattion_Beaconning_period = 10
cluster_rotation_period = 10

# alert position
alertx = 270
alerty = 110
Alert_RANGE = 90 # meters
Alert_increase_temp = 300
#TIME
ALERT_TIME = 119
ALERT_END = 300
## Runtime configuration
MAX_RUNTIME = 100


#aggregate time
AGGREGATE_TIME = 10

# node sensor range
COVERAGE_RADIUS = 15 # meters 

#ENERGY
#dead node threshold
DEAD_NODE_THRESHOLD = 0.299
LOW_NODE_THRESHOLD = 0.5
# node transmission energy cnsumption
PACKET_ENERGY_CONSUMPTION       = -0.00005
NODE_SLEEP_ENERGY_CONSUMPTION   = -0.00001
NODE_RUNING_ENERGY_CONSUMPTION  = -0.00002

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

# initial energy at every node's battery
INITIAL_ENERGY = 2000 # mili Joules

RESULTS_PATH = './results/'


