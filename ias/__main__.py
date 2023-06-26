import sys
from .computer import Computer
from .instruct import parse_memmap

comp = Computer()
comp.reset()

fn = sys.argv[1]

with open(fn) as f:
    input_str = f.read()
    comp.load(parse_memmap(input_str))
    comp.run()
