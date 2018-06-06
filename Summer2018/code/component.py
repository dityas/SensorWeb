import numpy
from scipy.signal import sawtooth
import logging
import matplotlib.pyplot as plotter


class Component:

    """
        Defines a single virtual component such as Disk, CPU, Mem etc.
    """

    def __init__(self, cycles=100):
        self.cycles = cycles

    def create_waveform(self, start, stop, noise):
        raise NotImplementedError

    def get_data(self, start, stop, noise=0.01):
        """
            Returns waveform described by create waveform and clips it between
            0 and 1.
        """
        data = numpy.clip(self.create_waveform(start, stop, noise),
                          a_min=0, a_max=1)

        return data


class CPU(Component):

    """
        Defines the CPU component.
    """

    def __init__(self, cycles):
        Component.__init__(self, cycles)
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.logger.debug("CPU component initialized")

    def create_waveform(self, start, stop, noise):
        indices = numpy.linspace(start=start,
                                 stop=stop,
                                 num=(stop-start) * 100)

        n = numpy.random.normal(size=indices.shape) * noise
        signal = numpy.sin(2 * numpy.pi * self.cycles * indices)
        signal = (signal / 2) + 0.5
        signal = signal + n
        return signal


class DiskIO(Component):
    """
        Defines the disk IO component.
    """

    def __init__(self, cycles):
        Component.__init__(self, cycles)
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.logger.debug("Disk IO component initialized")

    def create_waveform(self, start, stop, noise):
        indices = numpy.linspace(start=start,
                                 stop=stop,
                                 num=(stop-start) * 100)

        n = numpy.random.normal(size=indices.shape) * noise
        signal = sawtooth(2 * numpy.pi * self.cycles * indices)
        signal = (signal / 2) + 0.5
        signal = signal + n
        return signal


class Network(Component):
    """
        Defines the networking component.
    """

    def __init__(self, cycles):
        Component.__init__(self, cycles)
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.logger.debug("Networking component initialized")

    def create_waveform(self, start, stop, noise):
        indices = numpy.linspace(start=start,
                                 stop=stop,
                                 num=(stop-start) * 100)

        n = numpy.random.normal(size=indices.shape) * noise
        signal = sawtooth(2 * numpy.pi * self.cycles * indices, width=0.5)
        signal = (signal / 2) + 0.5
        signal = signal + n
        return signal
