import math

## Runtime configuration
MAX_RUNTIME = 500
#ALERT TIME
ALERT_TIME = 119
ALERT_END = 400

# area definition
AREA_WIDTH = 300
AREA_LENGTH = 200

#TDMA
CSMA_duration = 7
TDMA_duration = 3
Inactive_duration = 198

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


#aggregate time
AGGREGATE_TIME = 10

# node sensor range
COVERAGE_RADIUS = 15 # meters 

#ENERGY
# initial energy at every node's battery
INITIAL_ENERGY = 2000 # mili Joules 2000

P_TX = 0.084 * 100000  # Watts to transmite 
P_RX = 0.073 * 100000 # Watts to receive
#dead node threshold
DEAD_NODE_THRESHOLD = 0.299
LOW_NODE_THRESHOLD = 0.5

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
Multiframe_state = True


RESULTS_PATH = 'report/'


