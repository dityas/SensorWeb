#!/usr/bin/env python
import socket

# GLOBALS:
BIND_ADDRESS=('',5005)

class Listener:
    
    """
        Listens on port 5005 for data streams and then reads 2048 bytes of data.
    """

    def __init__(self):
        self.soc=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.soc.bind(BIND_ADDRESS)

    def write_to_file(self,data):
        f=open("data.txt","wb")
        f.write(data)
        f.flush()
        f.close()
            
    def run(self):

        """
            Runs forever. Listens on BIND_ADDRESS for data and then prints out data.
        """

        while 1:

            data,address=self.soc.recvfrom(2048)
            print("Got data from "+str(address))
            self.write_to_file(data)

if __name__=="__main__":
    listener=Listener()
    listener.run()
