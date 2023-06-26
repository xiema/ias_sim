import ias
from ias.utils import *


def test_load():
    comp = ias.Computer()
    comp.reset()
    with open("tests/memstate/memstate.txt") as f:
        program = ias.parse_memstate(f.read())
    comp.load(program)
    comp.run()

    comp.reset()
    with open("tests/memstate/memstate2.txt") as f:
        program = ias.parse_memstate(f.read())
    comp.load(program)
    comp.run()
