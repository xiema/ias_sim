from .instruct import instruction_info
from .utils import *


def _parse_mem(s):
    syms = s.split()
    val = 0
    if len(syms) == 1:
        val = toint(syms[0]) % pow2[40]
    elif len(syms) == 4:
        val = toint(syms[0]) + toint(syms[1]) * pow2[8] + \
            toint(syms[2]) * pow2[20] + toint(syms[3]) * pow2[28]
    else:
        raise SyntaxError(s)
    return val


def parse_snapshot(instr, shorthand=False):
    """
    Parses a memory snapshot to a list of ints
    """
    if type(instr) is not list:
        instr = get_lines(instr)
    translated = {}
    if shorthand:
        if type(instr) is not list:
            instr = get_lines(instr)
        translated = {}
        i = 0
        for ln in instr:
            if ln.startswith('='):
                i = int(ln[1:])
                continue
            translated[i] = _parse_mem(ln)
            i += 1
    else:
        for ln in instr:
            ln = ln.replace('\t', ' ')
            syms = ln.split()
            val = 0
            if len(syms) == 2:
                addr = int(syms[0], 16)
                val = int(syms[1], 16)
            elif len(syms) == 5:
                addr = int(syms[0], 16)
                val = int(syms[1], 16) + int(syms[2], 16) * pow2[8] + \
                    int(syms[3], 16) * pow2[20] + int(syms[4], 16) * pow2[28]
            else:
                raise SyntaxError(ln)
            translated[addr] = val

    return translated


def mc_to_asm(code):
    if type(code) is dict:
        code = [p[1] for p in sorted(code.items())]

    # separate instruction pairs per memory location
    unpaired = []
    for val in code:
        unpaired.append(val % pow2[20])
        unpaired.append(val >> 20)

    translated = []
    for val in unpaired:
        op = binslice(val, 20, 0, 7)
        oprnd = binslice(val, 20, 8, 19)
        instr = instruction_info[binstr(op, 8)]
        translated.append(instr.fmt.format(oprnd))

    return translated


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-m", "--machinecode", action="store_true")
    parser.add_argument("-s", "--snapshot", action="store_true")
    parser.add_argument("-l", "--lines", type=int)
    parser.add_argument("file")
    args = parser.parse_args()

    if args.snapshot:
        with open(args.file) as f:
            code = parse_snapshot(f.read())
        n = args.lines or (max(code.keys()) + 1)
        code = [p[1] for p in sorted(code.items())]
        asm = mc_to_asm(code[:n])
        print(asm)
