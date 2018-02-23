#!/usr/bin/env python
import socket
import time
import random
import os

### GLOBALS:

MAX_SLEEP=10
RANDOM_SIZE=2048

class BCaster:

    """
        Define broadcaster class.

        Randomly wake up and broadcast data.
    """

    def __init__(self):
        self.soc=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.soc.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

    def make_data(self):
        """
            Makes RANDOM_SIZE of random_data bytes.
        """
        return os.urandom(RANDOM_SIZE)

    def send_data(self,data):
        print("Sending "+str(data))
        self.soc.sendto(data,('192.168.1.255',5005))

    def run(self):

        """
            Run loop.
        """

        while 1:

            sleep_time=random.randint(1,MAX_SLEEP)
            print("Sleeping for "+str(sleep_time))
            time.sleep(sleep_time)

            data=self.make_data()
            self.send_data(data)

if __name__=="__main__":
    bcaster=BCaster()
    bcaster.run()
