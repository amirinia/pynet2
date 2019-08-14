import math
#TDMA
CSMA_duration = 9
TDMA_duration = 7
Inactive_duration = 14

# and config
BEACONING_TIME       = 5

#TIME
## Runtime configuration
MAX_RUNTIME = 100

#aggregate time
AGGREGATE_TIME = 10

# node sensor range
COVERAGE_RADIUS = 15 # meters 

#ENERGY
#dead node threshold
DEAD_NODE_THRESHOLD = 0.0099

# node transmission energy cnsumption
PACKET_ENERGY_CONSUMPTION       = -5
NODE_SLEEP_ENERGY_CONSUMPTION   = -1
NODE_RUNING_ENERGY_CONSUMPTION  = -2

#node CPU
NODE_AGGREGATE_ENERGY_CONSUMPTION = -2

# node transmission range node discovery
TX_RANGE = 100 # meters 30
BSID = -1

# area definition
AREA_WIDTH = 300
AREA_LENGTH = 200

# controller  position
BS_POS_X = 0.0
BS_POS_Y = 0.0

# packet configs
MSG_LENGTH = 4000 # bits
HEADER_LENGTH = 150 # bits

# initial energy at every node's battery
INITIAL_ENERGY = 2000 # mili Joules

RESULTS_PATH = './results/'


