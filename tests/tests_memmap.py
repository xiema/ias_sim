from random import randrange

import ias
from ias.utils import *


def rand(bitwidth):
    return randrange(2**bitwidth)


def test_simple_addition():
    comp = ias.Computer()
    comp.reset()
    comp.load(ias.parse_memmap("""
        0x1 1000 0x5 1001
        0x21 1002 0x0 0
        =1000
        1000
        20
    """))
    comp.run()
    assert (comp.REG.AC == 1020)
    assert (comp.MEM[1002] == 1020)
    # print(f"Simple Addition: {comp.instcount}")


def test_array_mult():
    comp = ias.Computer()
    comp.reset()
    ans = []
    program = ias.parse_memmap("""
        0x1 4000 0x5 4001
        0x13 4 0x5 4001
        0x12 5 0x5 4001
        0x13 5 0x5 4001
        0x13 6 0x9 0
        0xb 0 0x21 0
        0xa 0 0x21 0
        0x1 4000 0x6 4002
        0x21 4000 0x10 0
        0

        =4000
        0x0 0x0 0x0 499
        0x0 0x0 0x0 500
        0x0 0x0 0x0 1
    """)
    for i in range(500):
        a, b = rand(40), rand(40)
        ans.append(a*b)
        program[500+i] = a
        program[1000+i] = b
    comp.load(program)
    comp.run()
    for i in range(500):
        h, l = ans[i]//pow2[40], ans[i] % pow2[40]
        assert (h == comp.MEM[1500+i])
        assert (l == comp.MEM[2000+i])
    # print(f"Array Multiplication: {comp.instcount}")

def test_array_addition():
    comp = ias.Computer()
    comp.reset()
    ans = []
    program = ias.parse_memmap("""
        0x1 4000 0x5 4001
        0x13 3 0x5 4001
        0x12 4 0x5 4001
        0x13 4 0x1 0
        0x5 0 0x21 0
        0x1 4000 0x6 4002
        0x21 4000 0x10 0
        0

        =4000
        0x0 0x0 0x0 999
        0x0 0x0 0x0 1000
        0x0 0x0 0x0 0x1
    """)
    for i in range(1000):
        a, b = rand(40), rand(40)
        ans.append((a + b) % pow2[40])
        program[1000+i] = a
        program[2000+i] = b
    comp.load(program)
    comp.run()
    for i in range(1000):
        # if ans[i] != comp.MEM[3000+i]:
        #     print(ans[i], comp.MEM[3000+i])
        assert (ans[i] == comp.MEM[3000+i])
    # print(f"Array Addition: {comp.instcount}")


def test_array_addition2():
    comp = ias.Computer()
    comp.reset()
    ans = []
    program = ias.parse_memmap("""
        0x1 2999 0x5 3999
        0x21 1999 0x1 0
        0x6 5 0x21 0
        0x6 6 0x12 1
        0x6 7 0xf 0
        0x0 0x1 0x0 0x1
        0x1 2000 0x5 2000
        0x0 0x0 0x0 1000
    """)
    for i in range(1000):
        a, b = rand(40), rand(40)
        ans.append((a + b) % pow2[40])
        program[2000+i] = a
        program[3000+i] = b

    comp.load(program)
    comp.run()
    for i in range(1000):
        # if ans[i] != comp.MEM[3000+i]:
        #     print(ans[i], comp.MEM[3000+i])
        assert (ans[i] == comp.MEM[1000+i])
    # print(f"Array Addition: {comp.instcount}")

def test_array_mult2():
    comp = ias.Computer()
    comp.reset()
    ans = []
    program = ias.parse_memmap("""
        0x1 4000 0x5 4001
        0x13 4 0x5 4001
        0x12 5 0x5 4001
        0x13 5 0x5 4001
        0x13 6 0x9 0
        0xb 0 0x21 0
        0xa 0 0x21 0
        0x1 4000 0x6 4002
        0x21 4000 0x10 0
        0

        =4000
        0x0 0x0 0x0 499
        0x0 0x0 0x0 500
        0x0 0x0 0x0 1
    """)
    for i in range(500):
        a, b = rand(40), rand(40)
        ans.append(a*b)
        program[500+i] = a
        program[1000+i] = b
    comp.load(program)
    comp.run()
    for i in range(500):
        h, l = ans[i]//pow2[40], ans[i] % pow2[40]
        assert (h == comp.MEM[1500+i])
        assert (l == comp.MEM[2000+i])
    # print(f"Array Multiplication: {comp.instcount}")


def test_load_add():
    comp = ias.Computer()
    comp.reset()
    with open("tests/memmap/simple_add.txt") as f:
        program = ias.parse_memmap(f.read())
    with open("tests/memmap/simple_add_result.txt") as f:
        ans = ias.parse_memmap(f.read())
    comp.load(program)
    comp.run()
    for i in range(ias.MAINMEMORY_DEF[0]):
        assert (comp.MEM[i] == ans.get(i, 0))

