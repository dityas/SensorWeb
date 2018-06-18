#!/usr/bin/env python
import random
import time
import socket
import zlib
import cmath
import os
from multiprocessing import Process

BIND_ADDRESS = ('', 5005)

ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ssock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

rsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rsock.bind(BIND_ADDRESS)


def send_broadcast(data):
    ssock.sendto(data, ('192.168.1.255', 5005))


def write_data(filename, data):

    data = ",".join([str(i) for i in data])

    with open(filename, 'w') as f:
        f.write(data)
        f.write("\r\n")
        f.flush()


def read_data(filename):

    files = os.listdir(".")
    if filename not in files:
        return []

    with open(filename) as f:
        data = f.read().strip()
        data = [complex(i) for i in data.split(",")]

    return data


def sample_data(samples=500, stime=300):

    data = []
    sleep_time = (1.0 / samples)

    for i in range(samples * stime):
        data.append(random.randint(0, 255))
        time.sleep(sleep_time)

    return data


def DFT(numbers):
    pi2 = cmath.pi * 2
    fm_numbers = []

    N = len(numbers)
    for n in range(N):

        fm = 0.0

        for m in range(N):
            fm += numbers[n] * cmath.exp(-1j * pi2 * m * n / N)
        fm_numbers.append(fm)

    return fm_numbers


def compute_cc(series1, series2):

    if len(series1) != len(series2):
        return float('-inf')

    else:
        corr = 0.0
        for i in range(len(series1)):
            corr += (series1[i] * series2[i])

        #difference = (difference/len(series1))

    return corr


def process_request():

    print("Listener started. Going in to listen loop")
    while 1:

        # Get data and decompress
        data, address = rsock.recvfrom(100000)
        print("Got data")
        data = zlib.decompress(data)
        data = [complex(i) for i in data.split(",")]

        # Read from file
        my_data = read_data("data.txt")

        # Compute difference
        difference = compute_cc(data, my_data)

        # Write difference to file.
        name = str(address[0]).replace(".", "_") + "cc.txt"
        write_data(name, [difference])


def main():

    # Start listener thread
    p = Process(target=process_request)
    p.start()

    runs = 1
    while 1:

        # Sample data.
        data = sample_data(100, 10)
        transformed = DFT(data)

        # Write data to file.
        print("Got data. Writing to file.")
        write_data("data.txt", transformed)

        # Compress for transmission.
        strdata = ",".join([str(i) for i in transformed])
        compressed = zlib.compress(strdata)

        # Broadcast Data.
        print("Sending data.")
        send_broadcast(compressed)

        if runs % 10 == 0:
            runs = 1
            print("10 Runs over. Deleting storage.")
            os.system("rm data.txt")

        runs += 1


if __name__ == "__main__":
    main()
