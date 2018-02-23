#!/usr/bin/env python
import random
import os
import time

while 1:
    f = open('tempfile', 'wb')
    for i in range(1000000):
        data = bytes(random.randint(0, 255))
        f.write(data)
    f.flush()
    os.system("rm tempfile")
    time.sleep(2)
