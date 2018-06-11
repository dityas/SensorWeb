#!/usr/bin/env python
import argparse
import sys
import logging


sys.path.append("/home/adityas/UGA/SensorWeb/scripts/Summer2018/code")

from simulator.device import Device, DeviceState

parser = argparse.ArgumentParser()
parser.add_argument("s", action="store", help="sensitivity of EM")
parser.add_argument("i", action="store", type=int, help="number of \
                    iterations for data generation")
parser.add_argument("--logfile", action="store", help="write logs to"\
                    "thisfile")

args = parser.parse_args()

if args.logfile is not None:
    logging.basicConfig(level=logging.DEBUG, filename=args.logfile)
else:
    logging.basicConfig(level=logging.DEBUG)

if args.s == "high":
    send_over_network = DeviceState(cpu_cycles=2,
                                    network_cycles=10,
                                    disk_cycles=3,
                                    name="net_send",
                                    noise=0.1)

    compute = DeviceState(cpu_cycles=10,
                          network_cycles=1,
                          disk_cycles=1,
                          name="compute", noise=0.1)

    read_file = DeviceState(cpu_cycles=3,
                            disk_cycles=10,
                            network_cycles=1,
                            name="read", noise=0.1)

    state_seq = [compute, send_over_network, read_file]

    device = Device(device_sequence=state_seq)

    device.write_to_disk(iterations=args.i)
