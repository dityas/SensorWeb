import zlib
import random
import string
import time


def compress(target):
    return zlib.compress(target)


def expand(compressed):
    return zlib.decompress(compressed)

while 1:
    s = ""
    for i in range(10000):
        s += random.sample(string.printable,1)[0]
    compressed = compress(s)
    u = expand(compressed)
    print("Done!")
    time.sleep(1)
