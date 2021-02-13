REGISTER_DEFS = {
    'MBR': 40,
    'MAR': 12,
    'IR': 8,
    'IBR': 20,
    'PC': 12,
    'AC': 40,
    'MQ': 40,
}

MAINMEMORY_DEF = (4096, 40)

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

import re
from classes import *


instruction_info = {}
symbol_to_opcode = {}
for instrdef in filter(lambda x: len(x) > 0, INSTRUCTION_DEFS.split('\n')):
    desc = re.search(r"^(?P<type>.*?)\s*(?P<opcode>\d{8})\s*(?P<symbol>.*?)$", instrdef.strip())
    instruction_info[desc['opcode']] = Instruction(desc['type'], int(desc['opcode'],2), desc['symbol'])
    symbol_to_opcode[desc['symbol']] = desc['opcode']


def translate(instr):
    if type(instr) is not list:
        instr = [ln.strip() for ln in filter(lambda x: len(x)>0, instr.splitlines())]
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
            val = toint(syms[0]) + toint(syms[1]) * pow2[8] + toint(syms[2]) * pow2[20] + toint(syms[3]) * pow2[28]
        else:
            raise SyntaxError(ln)
        translated[i] = val
        i += 1
    return translated

class Computer:
    def __init__(self):
        #create registers
        self.REG = Memory()
        for id, width in REGISTER_DEFS.items():
            self.REG.addcell(id, width)
        #create main memory
        self.MEM = Memory()
        size, width = MAINMEMORY_DEF
        for i in range(size):
            self.MEM.addcell(i, width)

        #  cycle flags
        #l/r instruction?
        self.offsetPC = False
        #need fetch from main memory?
        self.nextIBR = False
        #exit program?
        self.terminate = False
        self.instcount = 0

    def load(self, tomem=None, toreg=None):
        if type(tomem) is list:
            self.MEM[:len(tomem)] = tomem
        elif type(tomem) is dict:
            for k,v in tomem.items():
                self.MEM[k] = v
        if type(toreg) is dict:
            for k,v in toreg.items():
                self.REG[k] = v

    def reset(self):
        #it all returns to nothing
        self.MEM.reset()
        self.REG.reset()
        self.offsetPC = False
        self.nextIBR = False
        self.terminate = False
        self.instcount = 0

    def run(self):
        self.terminate = False
        while not self.terminate:
            self.step()

    def step(self):
        self.fetch()
        self.execute()
        self.instcount += 1

    def fetch(self):
        if self.nextIBR:
            #next instruction is in IBR
            self.REG[['IR','MAR']] = self.REG['IBR',0:7, 'IBR',8:19]
            self.nextIBR = False
            self.REG.PC = self.REG.PC + 1
        else:
            #need fetch from main memory
            self.REG.MAR = self.REG.PC
            self.REG.MBR = self.MEM[self.REG.MAR]
            if self.offsetPC is False:
                #need to store right instruction in IBR
                self.REG[['IR','MAR','IBR']] = self.REG['MBR',0:7, 'MBR',8:19, 'MBR',20:39]
                self.nextIBR = True
            else:
                #discard left instruction
                self.REG[['IR','MAR']] = self.REG['MBR',20:27, 'MBR',28:39]
                self.REG.PC = self.REG.PC + 1
        #flip left-right
        self.offsetPC = not self.offsetPC

    def execute(self):
        opcode = self.REG.IR

        #still trying to think of a more elegant way of doing this...
        #LOAD MQ
        if opcode == 0b00001010:
            self.REG.AC = self.REG.MQ
        #LOAD MQ,M(X)
        elif opcode == 0b00001001:
            self.REG.MQ = self.MEM[self.REG.MAR]
        #STOR M(X)
        elif opcode == 0b00100001:
            self.MEM[self.REG.MAR] = self.REG.AC
        #LOAD M(X)
        elif opcode == 0b000000001:
            self.REG.AC = self.MEM[self.REG.MAR]
        #LOAD -M(X)
        elif opcode == 0b00000010:
            self.REG.AC = -self.MEM[self.REG.MAR]
        #LOAD |M(X)|
        elif opcode == 0b000000011:
            v = self.MEM[self.REG.MAR]
            if v < pow2[38]:
                self.REG.AC = v
            else:
                self.REG.AC = pow2[40] - v
        #LOAD -|M(X)|
        elif opcode == 0b000000100:
            v = self.MEM[self.REG.MAR]
            if v < pow2[38]:
                self.REG.AC = pow2[40] - v
            else:
                self.REG.AC = v
        #JUMP M(X,0:19)
        elif opcode == 0b000001101:
            self.REG.PC = self.REG.MAR
            self.offsetPC, self.nextIBR = False, False
        #JUMP M(X,20:39)
        elif opcode == 0b000001110:
            self.REG.PC = self.REG.MAR
            self.offsetPC, self.nextIBR = True, False
        #JUMP + M(X,0:19)
        elif opcode == 0b000001111:
            if self.REG.AC < pow2[38]:
                self.REG.PC = self.REG.MAR
                self.nextIBR, self.offsetPC = False, False
        #JUMP + M(X,20:39)
        elif opcode == 0b000010000:
            if self.REG.AC < pow2[38]:
                self.REG.PC = self.REG.MAR
                self.nextIBR, self.offsetPC = False, True
        #ADD M(X)
        elif opcode == 0b000000101:
            self.REG.AC = self.REG.AC + self.MEM[self.REG.MAR]
        #ADD |M(X)|
        elif opcode == 0b000000111:
            v = self.MEM[self.REG.MAR]
            if v < pow2[38]:
                self.REG.AC = self.REG.AC + v
            else:
                self.REG.AC = self.REG.AC + pow2[40] - v
        #SUB M(X)
        elif opcode == 0b000000110:
            self.REG.AC = self.REG.AC - self.MEM[self.REG.MAR]
        #SUB |M(X)|
        elif opcode == 0b000001000:
            v = self.MEM[self.REG.MAR]
            if v < pow2[38]:
                self.REG.AC = self.REG.AC - v
            else:
                self.REG.AC = self.REG.AC - pow2[40] + v
        #MUL M(X)
        elif opcode == 0b000001011:
            prod = self.MEM[self.REG.MAR] * self.REG.MQ
            self.REG['AC'] = prod // self.REG.cells['MQ'].uprbound
            self.REG['MQ'] = prod
        #DIV M(X)
        elif opcode == 0b000001100:
            self.REG.MQ, self.REG.AC = divmod(self.REG.AC, self.MEM[self.REG.MAR])
        #LSH
        elif opcode == 0b000010100:
            self.REG.AC = self.REG.AC << 1
        #RSH
        elif opcode == 0b000010101:
            self.REG.AC = self.REG.AC >> 1
        #STOR M(X,8:19)
        elif opcode == 0b000010010:
            self.MEM[self.REG.MAR, 8:19] = self.REG['AC', 28:39]
        #STOR M(X,28:39)
        elif opcode == 0b000010011:
            self.MEM[self.REG.MAR, 28:39] = self.REG['AC', 28:39]
        #EXIT
        elif opcode == 0b000000000:
            self.terminate = True