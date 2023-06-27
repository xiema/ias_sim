import ias
from ias.translate import *


def test_simple():
    code = parse_snapshot("""
        0x1 1000 0x5 1001
        0x21 1002 0x0 0
    """, True)
    asm = mc_to_asm(code)
    mc = asm_to_mc(asm)
    for i in range(len(code)):
        assert code[i] == mc[i]

    code = [
        "LOAD MQ", "STOR M(1000)",
        "LOAD M(1002)", "ADD M(2000)",
        "EXIT",
    ]
    mc = asm_to_mc(code)
    asm = mc_to_asm(mc)
    for i in range(len(code)):
        assert code[i] == asm[i]


def test_instruction_set():
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
        "EXIT": 0b0,
    }
    in_asm = list(d.keys())
    in_mc = [a + (b << 20) for a, b in pairs(d.values())]

    mc = asm_to_mc(in_asm)
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
    comp = ias.Computer()
    comp.reset()
    with open("tests/asm/simple_add.asm") as f:
        code = f.read()
    comp.load(parse_asm(code))
    comp.run()
    with open("tests/asm/simple_add_result.asm") as f:
        ans = parse_asm(f.read())
    for i in range(ias.MAINMEMORY_DEF[0]):
        try:
            assert comp.MEM[i] == ans.get(i, 0)
        except AssertionError as e:
            raise AssertionError(f"{i}: {comp.MEM[i]} != {ans.get(i, 0)}", e)
