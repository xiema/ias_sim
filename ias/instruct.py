import re
from collections import namedtuple

from .utils import *


INSTRUCTION_DEFS = """
Data transfer            00001010        LOAD MQ
Data transfer            00001001        LOAD MQ,M(X)
Data transfer            00100001        STOR M(X)
Data transfer            00000001        LOAD M(X)
Data transfer            00000010        LOAD -M(X)
Data transfer            00000011        LOAD |M(X)|
Data transfer            00000100        LOAD -|M(X)|
Unconditional branch     00001101        JUMP M(X,0:19)
Unconditional branch     00001110        JUMP M(X,20:39)
Conditional branch       00001111        JUMP + M(X,0:19)
Conditional branch       00010000        JUMP + M(X,20:39)
Arithmetic               00000101        ADD M(X)
Arithmetic               00000111        ADD |M(X)|
Arithmetic               00000110        SUB M(X)
Arithmetic               00001000        SUB |M(X)|
Arithmetic               00001011        MUL M(X)
Arithmetic               00001100        DIV M(X)
Arithmetic               00010100        LSH
Arithmetic               00010101        RSH
Address modify           00010010        STOR M(X,8:19)
Address modify           00010011        STOR M(X,28:39)
Exit                     00000000        EXIT
"""

INST_PATTERN = r"^(?P<type>.*?)\s*(?P<opcode>\d{8})\s*(?P<symbol>.*?)$"

Instruction = namedtuple('Instruction', ['type', 'opcode', 'symbol'])


instruction_info = {}
symbol_to_opcode = {}
for instrdef in filter(lambda x: len(x) > 0, INSTRUCTION_DEFS.split('\n')):
    desc = re.search(INST_PATTERN, instrdef.strip())
    instruction_info[desc['opcode']] = Instruction(
        desc['type'], int(desc['opcode'], 2), desc['symbol'])
    symbol_to_opcode[desc['symbol']] = desc['opcode']


def parse_bin(instr):
    """
    Parses binary shorthand to a list of ints
    """
    if type(instr) is not list:
        instr = [ln.strip()
                 for ln in filter(lambda x: len(x) > 0, instr.splitlines())]
    translated = {}
    i = 0
    for ln in instr:
        if ln.startswith('='):
            i = int(ln[1:])
            continue
        syms = ln.split(' ')
        val = 0
        if len(syms) == 1:
            val = toint(syms[0])
        elif len(syms) == 4:
            val = toint(syms[0]) + toint(syms[1]) * pow2[8] + \
                toint(syms[2]) * pow2[20] + toint(syms[3]) * pow2[28]
        else:
            raise SyntaxError(ln)
        translated[i] = val
        i += 1
    return translated
