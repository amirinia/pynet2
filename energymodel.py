
import math
import config

Power_Type = {0: "External", 1: "Battery", 2: "Energy Harvesting"}

#we use energy model of pymote 2.0 which uses 3 partsfunctions decrease_rx_energy decrease_tx_energy decrease_energy
class EnergyModel(object):
    P_TX = config.P_TX  # Watts to transmite 
    P_RX = config.P_RX  # Watts to receive

    E_INIT = config.INITIAL_ENERGY #2.0 * 1000  # 2 Joules
    E_MIN = 0.5   # Joules to operate

    # charging  rate
    P_CHARGING = 0.0005  # Watts

    # idle discharge rate
    P_IDLE = 0.001  # Watts

    # transmission rate
    TR_RATE = 250   # kbps

    def __init__(self, power_type=1, node_type=None, **kwargs):
        """
        Initialize the node object.
        node_type: 'N' regular, 'B' base station/Sink, 'C' coordinator/cluster head/relay

        power_type = 0 is for Base Station
        """
        self.type = node_type or 'N'
        self.power_type = power_type
        self.energy = self.E_INIT
        self.energy_consumption = 0

    def __repr__(self):
        return "<Power Type=%s, Energy=%d mJ>" % (Power_Type[self.power_type], self.energy)

    def decrease_tx_energy(self, packet_size):
        # power consumption = Tx power * Tx time
        tx_time = (packet_size * 8.0 / self.TR_RATE / 1024.0)
        energy_dec = self.P_TX * tx_time
        if self.power_type != 0:
            self.energy -= energy_dec
        self.energy_consumption += energy_dec
        return energy_dec, tx_time

    def decrease_rx_energy(self, packet_size):
        # power consumption = Rx power * Tx time
        tx_time = (packet_size * 8.0 / self.TR_RATE / 1024.0)
        energy_dec = self.P_RX * tx_time
        if self.power_type != 0:
            self.energy -= energy_dec
        self.energy_consumption += energy_dec
        return energy_dec, tx_time

    def decrease_energy(self, discharging_rate=None, discharging_time=1):
        energy_dec = (discharging_rate or self.P_IDLE) * discharging_time
        if self.power_type != 0:
            self.energy -= energy_dec
        self.energy_consumption += energy_dec
        return self.energy