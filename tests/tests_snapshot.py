import ias
from ias.utils import *


def test_load():
    comp = ias.Computer()
    comp.reset()
    with open("tests/snapshot/sample1.sn") as f:
        program = ias.parse_snapshot(f.read())
    comp.load(program)
    comp.run()

    comp.reset()
    with open("tests/snapshot/sample2.sn") as f:
        program = ias.parse_snapshot(f.read())
    comp.load(program)
    comp.run()


def test_array_add():
    comp = ias.Computer()
    comp.reset()
    with open("tests/snapshot/array_add.sn") as f:
        program = ias.parse_snapshot(f.read())
    comp.load(program)
    comp.run()

    with open("tests/snapshot/array_add_result.sn") as f:
        ans = ias.parse_snapshot(f.read())

    for i in range(ias.MAINMEMORY_DEF[0]):
        try:
            assert comp.MEM[i] == ans.get(i, 0)
        except AssertionError as e:
            raise AssertionError(f"{i}: {comp.MEM[i]} != {ans.get(i, 0)}", e)
