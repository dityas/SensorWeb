import logging
import numpy
import pandas
from component import CPU, DiskIO, Network
from energy_meter import HighSensitivityLinearEM, LowSensitivityLinearEM


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
        self.name = name
        self.noise = noise

        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def get_data(self, start, stop):
        cpu_samples = self.cpu.get_data(start=start, stop=stop,
                                        noise=self.noise)
        disk_samples = self.disk.get_data(start=start, stop=stop,
                                          noise=self.noise)
        network_samples = self.network.get_data(start=start, stop=stop,
                                                noise=self.noise)

        data = numpy.stack([cpu_samples,
                            disk_samples,
                            network_samples], axis=1)

        return pandas.DataFrame(data, columns=["cpu", "disk", "network"])


class Device:

    """
        Simulates a device with various states.
    """

    def __init__(self, device_sequence, data_dir="../data",
                 energy_meter=None, noise=0.01):
        self.sequence = device_sequence
        self.data_dir = data_dir
        self.noise = noise

        if energy_meter is None:
            self.energy_meter = HighSensitivityLinearEM()
        else:
            self.energy_meter = energy_meter

        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.logger.info(f"Device initialised")

    def run(self):
        data = []
        for state in self.sequence:
            self.logger.debug(f"Device in state {state.name}")
            state_data = state.get_data(start=1, stop=2)
            state_data = self.energy_meter.get_data(state_data)
            data.append(state_data)

        return pandas.concat(data, ignore_index=True)
