import ias
from random import randrange
from utils import *

def rand(bitwidth):
    return randrange(2**bitwidth)

def fmt(i, v):
    addr = format(i, '03X')
    i1a = format(v % pow2[8], '02X')
    i1b = format(v % pow2[20] // pow2[8], '03X')
    i2a = format(v % pow2[28] // pow2[20], '02X')
    i2b = format(v // pow2[28], '03X')
    return f"{addr} {i1a} {i1b} {i2a} {i2b}\n"

comp = ias.Computer()

comp.reset()
test_array_addition2 = """
0x1 1999 0x5 2999
0x21 3999 0x1 0
0x6 6 0x21 0
0x5 7 0x12 1
0x6 8 0xf 0
0xd 0x400 0 0
0x0 0x1 0x0 0x1
0x0 0x0 0x0 1000
0x1 1000 0x5 3000
"""
ans = []
translated = ias.translate(test_array_addition2)
for i in range(100):
    a,b = rand(40),rand(40)
    ans.append((a + b) % pow2[40])
    translated[200+i] = a
    translated[300+i] = b
with open("memmap2.txt", 'w') as f:
    for i, v in translated.items():
        f.write(fmt(i,v))
