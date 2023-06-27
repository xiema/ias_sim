import re
from collections import namedtuple

from .utils import *


INSTRUCTION_DEFS = """
Data transfer            00001010        LOAD MQ
Data transfer            00001001        LOAD MQ,M({})
Data transfer            00100001        STOR M({})
Data transfer            00000001        LOAD M({})
Data transfer            00000010        LOAD -M({})
Data transfer            00000011        LOAD |M({})|
Data transfer            00000100        LOAD -|M({})|
Unconditional branch     00001101        JUMP M({},0:19)
Unconditional branch     00001110        JUMP M({},20:39)
Conditional branch       00001111        JUMP + M({},0:19)
Conditional branch       00010000        JUMP + M({},20:39)
Arithmetic               00000101        ADD M({})
Arithmetic               00000111        ADD |M({})|
Arithmetic               00000110        SUB M({})
Arithmetic               00001000        SUB |M({})|
Arithmetic               00001011        MUL M({})
Arithmetic               00001100        DIV M({})
Arithmetic               00010100        LSH
Arithmetic               00010101        RSH
Address modify           00010010        STOR M({},8:19)
Address modify           00010011        STOR M({},28:39)
Exit                     11111111        EXIT
Skip                     10101010        SKIP
"""

INST_PATTERN = r"^[ \t]*(?P<type>.*?)[ \t]+(?P<opcode>\d{8})[ \t]+(?P<symbol>.*?)[ \t]*$"

Instruction = namedtuple('Instruction', ['type', 'opcode', 'symbol', 'format', 'pattern'])


instruction_info = {}
symbol_to_opcode = {}
for instrdef in filter(lambda x: len(x) > 0, INSTRUCTION_DEFS.split('\n')):
    desc = re.search(INST_PATTERN, instrdef.strip())
    if desc is None:
        continue
    instruction_info[desc['opcode']] = Instruction(
        desc['type'], int(desc['opcode'], 2),
        desc['symbol'].format('X'), desc['symbol'],
        re.compile(re.escape(desc['symbol']).replace(r'\{\}', r'(\w+)') + "$")
    )
    symbol_to_opcode[desc['symbol']] = desc['opcode']
