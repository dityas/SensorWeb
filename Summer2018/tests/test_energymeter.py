import unittest
import sys
import numpy
import pandas

sys.path.append("/home/adityas/UGA/SensorWeb/scripts/Summer2018/code")

from device import DeviceState
from energy_meter import LowSensitivityLinearEM, HighSensitivityLinearEM


class TestEnergyMeter(unittest.TestCase):

    def setUp(self):
        self.send_over_network = DeviceState(cpu_cycles=2,
                                             network_cycles=10,
                                             disk_cycles=3,
                                             name="net_send")

        self.compute = DeviceState(cpu_cycles=10,
                                   network_cycles=1,
                                   disk_cycles=1,
                                   name="compute")

        self.read_file = DeviceState(cpu_cycles=3,
                                     disk_cycles=10,
                                     network_cycles=1,
                                     name="read")

        self.highEM = HighSensitivityLinearEM()
        self.lowEM = LowSensitivityLinearEM()

    def test_low_EM_scale(self):

        data = self.send_over_network.get_data(start=1, stop=2)
        # data = pandas.DataFrame(data, columns=["cpu", "disk", "network"])
        data = self.lowEM.get_data(data)
        self.assertTrue(numpy.max(data.as_matrix()) <= 1.0 and
                        numpy.min(data.as_matrix()) >= 0.0)

        data = self.compute.get_data(start=1, stop=2)
        # data = pandas.DataFrame(data, columns=["cpu", "disk", "network"])
        data = self.lowEM.get_data(data)
        self.assertTrue(numpy.max(data.as_matrix()) <= 1.0 and
                        numpy.min(data.as_matrix()) >= 0.0)

        data = self.read_file.get_data(start=1, stop=2)
        # data = pandas.DataFrame(data, columns=["cpu", "disk", "network"])
        data = self.lowEM.get_data(data)
        self.assertTrue(numpy.max(data.as_matrix()) <= 1.0 and
                        numpy.min(data.as_matrix()) >= 0.0)

    def test_high_EM_scale(self):

        data = self.send_over_network.get_data(start=1, stop=2)
        data = pandas.DataFrame(data, columns=["cpu", "disk", "network"])
        data = self.highEM.get_data(data)
        self.assertTrue(numpy.max(data.as_matrix()) <= 1.0 and
                        numpy.min(data.as_matrix()) >= 0.0)

        data = self.compute.get_data(start=1, stop=2)
        data = pandas.DataFrame(data, columns=["cpu", "disk", "network"])
        data = self.highEM.get_data(data)
        self.assertTrue(numpy.max(data.as_matrix()) <= 1.0 and
                        numpy.min(data.as_matrix()) >= 0.0)

        data = self.read_file.get_data(start=1, stop=2)
        data = pandas.DataFrame(data, columns=["cpu", "disk", "network"])
        data = self.highEM.get_data(data)
        self.assertTrue(numpy.max(data.as_matrix()) <= 1.0 and
                        numpy.min(data.as_matrix()) >= 0.0)
