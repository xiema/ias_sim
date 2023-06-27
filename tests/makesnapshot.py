import sys
sys.path.insert(0, "./")

import ias
from random import randrange
from ias.utils import *


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
0x1 199 0x5 299
0x21 399 0x1 0
0x6 6 0x21 0
0x5 7 0x12 1
0x6 8 0xf 0
0xd 400 0 0
0x0 0x1 0x0 0x1
0x0 0x0 0x0 100
0x1 100 0x5 300
"""
translated = ias.parse_snapshot(test_array_addition2)
ans = translated.copy()
for i in range(100):
    a, b = rand(40), rand(40)
    ans[300+i] = (a + b) % pow2[40]
    ans[100+i] = translated[100+i] = a
    ans[200+i] = translated[200+i] = b
# ans.update(translated)

test_array_addition2 = """
0x1 99 0x5 199
0x21 299 0x1 0
0x6 6 0x21 0
0x5 7 0x12 1
0x6 8 0xf 0
0xd 400 0 0
0x0 0x1 0x0 0x1
0x0 0x0 0x0 100
0x1 100 0x5 300
"""
ans.update(ias.parse_snapshot(test_array_addition2))

with open("tests/snapshot/array_add.sn", 'w') as f:
    for i, v in sorted(translated.items()):
        f.write(fmt(i, v))
with open("tests/snapshot/array_add_result.sn", 'w') as f:
    for i, v in sorted(ans.items()):
        f.write(fmt(i, v))
