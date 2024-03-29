import ias
from ias.translate import *
from ias.assemble import Assembler


def test_simple():
    """
    Simple test translating back and forth from assembly and machine code.
    """

    assembler = Assembler()

    code = parse_snapshot("""
        0x1 1000 0x5 1001
        0x21 1002 0xFF 0
    """, True)
    asm = mc_to_asm(code)
    mc = assembler.asm_to_mc(asm)
    for i in range(len(code)):
        try:
            assert code[i] == mc[i]
        except AssertionError as e:
            raise AssertionError(f"{i}: {code[i]} != {mc[i]}", e)

    code = [
        "LOAD MQ", "STOR M(1000)",
        "LOAD M(1002)", "ADD M(2000)",
        "EXIT",
    ]
    mc = assembler.asm_to_mc(code)
    asm = mc_to_asm(mc)
    for i in range(len(code)):
        assert code[i] == asm[i]


def test_instruction_set():
    """
    Test translation back and forth of all instructions
    """
    
    x = 1234 << 8
    d = {
        "LOAD MQ": 0b1010,
        "LOAD MQ,M(1234)": 0b1001 + x,
        "STOR M(1234)": 0b100001 + x,
        "LOAD M(1234)": 0b1 + x,
        "LOAD -M(1234)": 0b10 + x,
        "LOAD |M(1234)|": 0b11 + x,
        "LOAD -|M(1234)|": 0b100 + x,
        "JUMP M(1234,0:19)": 0b1101 + x,
        "JUMP M(1234,20:39)": 0b1110 + x,
        "JUMP + M(1234,0:19)": 0b1111 + x,
        "JUMP + M(1234,20:39)": 0b10000 + x,
        "ADD M(1234)": 0b101 + x,
        "ADD |M(1234)|": 0b111 + x,
        "SUB M(1234)": 0b110 + x,
        "SUB |M(1234)|": 0b1000 + x,
        "MUL M(1234)": 0b1011 + x,
        "DIV M(1234)": 0b1100 + x,
        "LSH": 0b10100,
        "RSH": 0b10101,
        "STOR M(1234,8:19)": 0b10010 + x,
        "STOR M(1234,28:39)": 0b10011 + x,
        "EXIT": 0b11111111,
    }
    in_asm = list(d.keys())
    in_mc = [a + (b << 20) for a, b in pairs(d.values())]

    assembler = Assembler()
    mc = assembler.asm_to_mc(in_asm)
    for i in range(len(in_mc)):
        try:
            assert in_mc[i] == mc[i]
        except AssertionError as e:
            raise AssertionError(f"{i}: {in_mc[i]} != {mc[i]}", e)

    asm = mc_to_asm(mc)
    for i in range(len(in_asm)):
        try:
            assert in_asm[i] == asm[i]
        except AssertionError as e:
            raise AssertionError(f"{i}: {in_asm[i]} != {asm[i]}", e)


def test_load():
    """
    Test loading from a .asm file
    """
    
    comp = ias.Computer()
    comp.reset()
    with open("tests/asm/simple_add.asm") as f:
        code = f.read()
    assembler = Assembler()
    comp.load(assembler.parse_asm(code))
    comp.run()
    with open("tests/asm/simple_add_result.asm") as f:
        ans = assembler.parse_asm(f.read())
    for i in range(ias.MAINMEMORY_DEF[0]):
        try:
            assert comp.MEM[i] == ans.get(i, 0)
        except AssertionError as e:
            raise AssertionError(f"{i}: {comp.MEM[i]} != {ans.get(i, 0)}", e)


def test_arithmetic():
    """
    Test arithmetic instructions for correctness
    """

    comp = ias.Computer()
    comp.reset()
    with open("tests/asm/arithmetic.asm") as f:
        code = f.read()
    assembler = Assembler()
    comp.load(assembler.parse_asm(code))
    comp.run()
    assert comp.MEM[4095] == 0

    # Manually check stored results
    for i in range(13):
        try:
            assert comp.MEM[2000 + i] == comp.MEM[3000 + i]
        except AssertionError as e:
            raise AssertionError(
                f"{i}: {comp.MEM[2000 + i]} != {comp.MEM[3000 + i]}", e)


def test_array():
    """
    Test array manipulation programs
    """
    
    comp = ias.Computer()
    assembler = Assembler()
    
    # Array addition with explicit alignment
    comp.reset()
    with open("tests/asm/array_add.asm") as f:
        code = f.read()
    comp.load(assembler.parse_asm(code))
    comp.run()
    assert comp.MEM[4095] == 0

    # Manually check stored results
    for i in range(5):
        try:
            assert comp.MEM[3000 + i] == comp.MEM[4000 + i]
        except AssertionError as e:
            raise AssertionError(
                f"{i}: {comp.MEM[3000 + i]} != {comp.MEM[4000 + i]}", e)

    # Array multiplication with implicit alignment
    comp.reset()
    with open("tests/asm/array_mult.asm") as f:
        code = f.read()
    comp.load(assembler.parse_asm(code))
    comp.run()
    assert comp.MEM[4095] == 0

    # Manually check stored results
    for i in range(5):
        try:
            assert comp.MEM[3000 + i] == comp.MEM[4000 + i]
        except AssertionError as e:
            raise AssertionError(
                f"{i}: {comp.MEM[3000 + i]} != {comp.MEM[4000 + i]}", e)


def test_advanced():
    comp = ias.Computer()
    assembler = Assembler()
    
    comp.reset()
    with open("tests/asm/fibonacci_series.asm") as f:
        code = f.read()
    comp.load(assembler.parse_asm(code))
    comp.run()
    assert comp.MEM[4095] == 0

    # Manually check stored results
    fibs = [0, 1]
    while len(fibs) < 20:
        fibs.append(fibs[-1] + fibs[-2])
    for i in range(len(fibs)):
        assert fibs[i] == comp.MEM[1000 + i]

    comp.reset()
    with open("tests/asm/align_test.asm") as f:
        code = f.read()
    comp.load(assembler.parse_asm(code))
    comp.run()
    try:
        assert comp.MEM[4095] == 0
    except AssertionError as e:
        raise AssertionError(f"status={comp.MEM[4095]}", e)

