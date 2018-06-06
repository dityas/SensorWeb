import unittest
import sys
import matplotlib.pyplot as plotter
import numpy

sys.path.append("/home/adityas/UGA/SensorWeb/scripts/Summer2018/code")

from component import CPU, DiskIO, Network


class TestComponents(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU(cycles=5)
        self.disk = DiskIO(cycles=5)
        self.network = Network(cycles=5)

    def test_cpu_length(self):
        cpu_data = self.cpu.get_data(start=0, stop=1, noise=0.01)
        self.assertEqual(cpu_data.shape[0], 100)

    def test_disk_length(self):
        cpu_data = self.disk.get_data(start=0, stop=1, noise=0.01)
        self.assertEqual(cpu_data.shape[0], 100)

    def test_network_length(self):
        cpu_data = self.network.get_data(start=0, stop=1, noise=0.01)
        self.assertEqual(cpu_data.shape[0], 100)

    def test_visualize(self):
        cpu_data = self.cpu.get_data(start=0, stop=1, noise=0.01)
        disk_data = self.disk.get_data(start=0, stop=1, noise=0.01)
        network_data = self.network.get_data(start=0, stop=1, noise=0.01)
        plotter.plot(cpu_data)
        plotter.plot(disk_data)
        plotter.plot(network_data)
        plotter.show()


if __name__ == "__main__":
    unittest.main()
