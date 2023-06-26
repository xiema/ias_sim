from .instruct import instruction_info
from .utils import *


def _parse_mem(s):
    syms = s.split()
    val = 0
    if len(syms) == 1:
        val = toint(syms[0])
    elif len(syms) == 4:
        val = toint(syms[0]) + toint(syms[1]) * pow2[8] + \
            toint(syms[2]) * pow2[20] + toint(syms[3]) * pow2[28]
    else:
        raise SyntaxError(s)
    return val


def parse_memstate(instr):
    """
    Parses a memory state to a list of ints
    """
    if type(instr) is not list:
        instr = get_lines(instr)
    translated = {}
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


def parse_memmap(instr):
    """
    Parses a memory map to a list of ints
    """
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
        translated.append(instr.format.format(oprnd))

    return translated


def _encode(instr):
    for info in instruction_info.values():
        m = info.pattern.match(instr)
        if m:
            if m.groups():
                return info.opcode + (toint(m[1]) << 8)
            else:
                return info.opcode
    else:
        raise SyntaxError(instr)


def asm_to_mc(code):
    encoded = [_encode(instr) for instr in code]
    if len(encoded) % 2:
        encoded.append(0)
    return [(a + (b << 20)) for a, b in pairs(encoded)]


def parse_asm(s):
    lines = get_lines(s)
    section = None
    translated = {}
    pos, ofs = 0, False
    for line in lines:
        if line in ['.text', '.data']:
            section = line
            pos, ofs = 0, False
            continue

        if section == '.text':
            if ofs:
                translated[pos] += _encode(line) << 20
                pos += 1
            else:
                translated[pos] = _encode(line)
            ofs = not ofs
        elif section == '.data':
            if line.startswith('='):
                pos = toint(line[1:])
                continue
            translated[pos] = _parse_mem(line)
            pos += 1

    return translated
