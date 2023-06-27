import sys
from .computer import Computer, MAINMEMORY_DEF
from .translate import parse_snapshot, parse_asm

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-s", "--snapshot", action="store_true")
parser.add_argument("--shorthand", action="store_true")
parser.add_argument("-a", "--asm", action="store_true")
parser.add_argument("--dump", action="store_true")
parser.add_argument("file")

args = parser.parse_args()

comp = Computer()
comp.reset()

with open(args.file) as f:
    input_str = f.read()
    code = None
    if args.snapshot:
        code = parse_snapshot(input_str, args.shorthand)
    elif args.asm:
        code = parse_asm(input_str)
    
    if code is not None:
        comp.load(code)
        comp.run()
        if args.dump:
            out = []
            for addr in range(MAINMEMORY_DEF[0]):
                o1, a1, o2, a2 = comp.MEM[addr, 0:7, addr, 8:19, addr, 20:27, addr, 28:39]
                out.append(f"{addr:03x} {o1:02x} {a1:03x} {o2:02x} {a2:03x}")
            print("\n".join(out).upper())
    else:
        exit(1)
