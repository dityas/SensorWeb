import unittest
import sys
import matplotlib.pyplot as plotter

sys.path.append("/home/adityas/UGA/SensorWeb/scripts/Summer2018/code")

from device import DeviceState, Device
from energy_meter import LowSensitivityLinearEM, HighSensitivityLinearEM


class TestEnergyMeter(unittest.TestCase):

    def setUp(self):
        self.send_over_network = DeviceState(cpu_cycles=2,
                                             network_cycles=10,
                                             disk_cycles=3,
                                             name="net_send",
                                             noise=0.1)

        self.compute = DeviceState(cpu_cycles=10,
                                   network_cycles=1,
                                   disk_cycles=1,
                                   name="compute", noise=0.1)

        self.read_file = DeviceState(cpu_cycles=3,
                                     disk_cycles=10,
                                     network_cycles=1,
                                     name="read", noise=0.1)

        state_seq = [self.compute, self.send_over_network, self.read_file]

        self.device = Device(device_sequence=state_seq)

    def test_device_run(self):
        data = self.device.run()
        print(data.describe())

    def test_visualise_data(self):
        data = self.device.run()
        plotter.subplot(411)
        plotter.plot(data["cpu"])
        plotter.ylim(0, 1)
        plotter.subplot(412)
        plotter.plot(data["disk"])
        plotter.ylim(0, 1)
        plotter.subplot(413)
        plotter.plot(data["network"])
        plotter.ylim(0, 1)
        plotter.subplot(414)
        plotter.plot(data["energy"])
        plotter.ylim(0, 1)
        plotter.show()
