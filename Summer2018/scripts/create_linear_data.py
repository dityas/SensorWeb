#!/usr/bin/env python
import argparse
import sys
import logging


sys.path.append("/home/adityas/UGA/SensorWeb/scripts/Summer2018/code")

from simulator.device import Device, DeviceState
from simulator.energy_meter import LowSensitivityLinearEM
from simulator.energy_meter import HighSensitivityNonLinearEM

parser = argparse.ArgumentParser()
parser.add_argument("s", action="store", help="sensitivity of EM")
parser.add_argument("c", action="store", help="complexity of EM")
parser.add_argument("i", action="store", type=int, help="number of" \
                    " iterations for data generation")
parser.add_argument("--logfile", action="store", help="write logs to" \
                    "thisfile")
parser.add_argument("data", action="store", help="Directory to store data")

args = parser.parse_args()

if args.logfile is not None:
    logging.basicConfig(level=logging.DEBUG, filename=args.logfile)
else:
    logging.basicConfig(level=logging.DEBUG)

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


if args.c == "linear":
    if args.s == "high":
        device = Device(device_sequence=state_seq,
                        data_dir=args.data)

    elif args.s == "low":
        device = Device(device_sequence=state_seq,
                        energy_meter=LowSensitivityLinearEM(),
                        data_dir=args.data)

elif args.c == "nonlinear":
    if args.s == "high":
        device = Device(device_sequence=state_seq,
                        data_dir=args.data,
                        energy_meter=HighSensitivityNonLinearEM())

elif args.c == "single":
    if args.s == "low":
        device = Device(device_sequence=[compute],
                        data_dir=args.data,
                        energy_meter=LowSensitivityLinearEM())


device.write_to_disk(iterations=args.i)
