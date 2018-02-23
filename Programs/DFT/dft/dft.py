#!/usr/bin/env python
import random
import cmath
import time

pi2 = cmath.pi * 2


def DFT(numbers):
    fm_numbers = []

    N = len(numbers)
    for n in range(N):

        fm = 0.0

        for m in range(N):
            fm += numbers[n] * cmath.exp(-1j * pi2 * m * n / N)
        fm_numbers.append(fm)

    return fm_numbers


while 1:
    data = [random.randint(1,255) for i in range(1000)]
    print(DFT(list(map(int, data))))
    time.sleep(1)
