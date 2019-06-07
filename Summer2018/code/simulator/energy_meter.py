import logging
import numpy


class EnergyMeter:

    """
        Base class for defining energy meter.
    """

    def __init__(self):
        pass

    def compute_energy(self,
                       cpu,
                       network,
                       disk):
        """
            Defines relation between collectd and energy.
        """

        raise NotImplementedError

    def get_data(self, readings):
        """
            Appends energy column to readings and returns it.
        """
        cpu = readings["cpu"]
        disk = readings["disk"]
        network = readings["network"]

        readings["energy"] = self.compute_energy(cpu=cpu,
                                                 network=network,
                                                 disk=disk)

        return readings


class LowSensitivityLinearEM(EnergyMeter):

    """
        Defines EM which reacts less to fluctations in collectd and has linear
        relationship between energy and collectd.
    """

    def __init__(self):
        self.cpu_factor = numpy.random.normal(0.1, 0.01)
        self.disk_factor = numpy.random.normal(0.1, 0.01)
        self.network_factor = numpy.random.normal(0.1, 0.01)
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        self.logger.info(f"Energy meter init with factors" \
                         f"cpu:{self.cpu_factor} + disk:{self.disk_factor} +" \
                         f"net:{self.network_factor}")

    def compute_energy(self, cpu, network, disk):
        energy = 0.5 + (self.cpu_factor * cpu) + \
                 (self.disk_factor * disk) + \
                 (self.network_factor * network)

        return energy


class HighSensitivityLinearEM(EnergyMeter):

    """
        Defines EM which reacts more to fluctations in collectd and has linear
        relationship between energy and collectd.
    """

    def __init__(self):
        self.cpu_factor = numpy.random.normal(0.25, 0.01)
        self.disk_factor = numpy.random.normal(0.25, 0.01)
        self.network_factor = numpy.random.normal(0.25, 0.01)

        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        self.logger.info(f"Energy meter init with factors "\
                         f"cpu:{self.cpu_factor} + disk:{self.disk_factor} + "\
                         f"net:{self.network_factor}")

    def compute_energy(self, cpu, network, disk):
        energy = 0.01 + (self.cpu_factor * cpu) + \
                 (self.disk_factor * disk) + \
                 (self.network_factor * network)

        return energy


class HighSensitivityNonLinearEM(EnergyMeter):

    """
        Defines EM which reacts more to fluctations in collectd and has linear
        relationship between energy and collectd.
    """

    def __init__(self):
        self.cpu_factor = numpy.random.normal(0.25, 0.01)
        self.disk_factor = numpy.random.normal(0.25, 0.01)
        self.network_factor = numpy.random.normal(0.25, 0.01)

        self.cpu_pow = numpy.random.randint(1, 3)
        self.disk_pow = numpy.random.randint(1, 3)
        self.network_pow = numpy.random.randint(1, 3)

        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        self.logger.info(f"Energy meter init with factors "\
                         f"cpu:{self.cpu_factor}^{self.cpu_pow} +"\
                         f"disk:{self.disk_factor}^{self.disk_pow} +"\
                         f"net:{self.network_factor}^{self.network_pow}")

    def compute_energy(self, cpu, network, disk):
        energy = 0.01 + (self.cpu_factor * cpu ** self.cpu_pow) + \
                 (self.disk_factor * disk ** self.disk_pow) + \
                 (self.network_factor * network ** self.network_pow)

        return energy
