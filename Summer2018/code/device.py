import logging
import numpy
from component import CPU, DiskIO, Network


class DeviceState:

    """
        Defines a state in the FSM of the device.
    """

    def __init__(self,
                 cpu_cycles,
                 disk_cycles,
                 network_cycles,
                 noise=0.1,
                 name="undefined state"):

        self.cpu = CPU(cycles=cpu_cycles)
        self.disk = DiskIO(cycles=disk_cycles)
        self.network = Network(cycles=network_cycles)

        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def get_data(self, start, stop):
        cpu_samples = self.cpu.get_data(start=start, stop=stop)
        disk_samples = self.disk.get_data(start=start, stop=stop)
        network_samples = self.network.get_data(start=start, stop=stop)

        data = numpy.stack([cpu_samples,
                            disk_samples,
                            network_samples], axis=1)

        return data


class Device:

    """
        Simulates a device with various states.
    """

    def __init__(self)
