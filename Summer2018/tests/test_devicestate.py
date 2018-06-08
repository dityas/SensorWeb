import unittest
import sys
import numpy

sys.path.append("/home/adityas/UGA/SensorWeb/scripts/Summer2018/code")

from device import DeviceState


class TestDeviceState(unittest.TestCase):

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

    def test_data_scale(self):
        for i in range(3):
            data = self.send_over_network.get_data(start=i, stop=i+1)
            self.assertTrue(numpy.max(data.as_matrix()) <= 1.0 and
                            numpy.min(data.as_matrix()) >= 0.0)
            data = self.compute.get_data(start=i, stop=i+1)
            self.assertTrue(numpy.max(data.as_matrix()) <= 1.0 and
                            numpy.min(data.as_matrix()) >= 0.0)
            data = self.read_file.get_data(start=i, stop=i+1)
            self.assertTrue(numpy.max(data.as_matrix()) <= 1.0 and
                            numpy.min(data.as_matrix()) >= 0.0)

    def test_data_shape(self):
        for i in range(1):
            data = self.send_over_network.get_data(start=i, stop=i+1)
            print(data.shape)
            data = self.compute.get_data(start=i, stop=i+1)
            print(data.shape)
            data = self.read_file.get_data(start=i, stop=i+1)
            print(data.shape)
