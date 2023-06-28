import re

from .utils import *


INSTRUCTION_DEFS = """
Data transfer            00001010        LOAD MQ             &   lm
Data transfer            00001001        LOAD MQ,M({})       &   lam {}
Data transfer            00100001        STOR M({})          &   sa {}
Data transfer            00000001        LOAD M({})          &   la {}
Data transfer            00000010        LOAD -M({})         &   la -{}
Data transfer            00000011        LOAD |M({})|        &   la |{}
Data transfer            00000100        LOAD -|M({})|       &   la -|{}
Unconditional branch     00001101        JUMP M({},0:19)     &   jl {}
Unconditional branch     00001110        JUMP M({},20:39)    &   jr {}
Conditional branch       00001111        JUMP + M({},0:19)   &   bl {}
Conditional branch       00010000        JUMP + M({},20:39)  &   br {}
Arithmetic               00000101        ADD M({})           &   add {}
Arithmetic               00000111        ADD |M({})|         &   add |{}
Arithmetic               00000110        SUB M({})           &   sub {}
Arithmetic               00001000        SUB |M({})|         &   sub |{}
Arithmetic               00001011        MUL M({})           &   mul {}
Arithmetic               00001100        DIV M({})           &   div {}
Arithmetic               00010100        LSH                 &   lsh
Arithmetic               00010101        RSH                 &   rsh
Address modify           00010010        STOR M({},8:19)     &   sal {}
Address modify           00010011        STOR M({},28:39)    &   sar {}
Exit                     11111111        EXIT                &   exit
Skip                     10101010        SKIP                &   skip
"""

INST_PATTERN = r"^[ \t]*(?P<type>.*?)[ \t]+(?P<opcode>\d{8})[ \t]+(?P<symbol>.*?)[ \t]+&[ \t]+(?P<alias>.*?)[ \t]*$"


class Instruction():
    def __init__(self, instr_type, opcode, fmt, alias):
        self.instr_type = instr_type
        self.opcode = int(opcode, 2)
        self.fmt = fmt
        self.symbol = fmt.format("X")
        self.pattern = re.compile(self._topattern(fmt))
        self.alias_fmt = alias
        self.alias_pattern = re.compile(self._topattern(alias))

    @classmethod
    def _topattern(cls, s):
        return re.escape(s).replace(r"\{\}", r"(\w+)") + "$"


instruction_info = {}
symbol_to_opcode = {}
for instrdef in filter(lambda x: len(x) > 0, INSTRUCTION_DEFS.split('\n')):
    desc = re.search(INST_PATTERN, instrdef.strip())
    if desc is None:
        continue
    instruction_info[desc['opcode']] = Instruction(
        desc['type'], desc['opcode'], desc['symbol'], desc['alias'])
    symbol_to_opcode[desc['symbol']] = desc['opcode']
