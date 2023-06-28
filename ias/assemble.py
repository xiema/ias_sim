import re

from .instruct import instruction_info, symbol_to_opcode
from .utils import toint, get_lines, pairs
from .translate import _parse_mem


class Assembler():

    pseudo_instructions = [
        # (PATTERN, LEFT-ALIGNED INSTR, RIGHT-ALIGNED INSTR)
        # auto-aligned jump
        (re.compile(r"ja (\w+)"), "JUMP M({},0:19)", "JUMP M({},20:39)"),
        # auto-aligned branch
        (re.compile(r"ba (\w+)"), "JUMP + M({},0:19)", "JUMP + M({},20:39)"),
        # auto-aligned store
        (re.compile(r"saa (\w+)"), "STOR M({},8:19)", "STOR M({},28:39)"),
    ]

    def __init__(self):
        self.symbol_table = {}

    def _encode(self, instr):
        for pat, opcodeL, opcodeR in self.pseudo_instructions:
            m = pat.match(instr)
            if m:
                addr, addr_ofs = self.symbol_table[m[1]]
                opcode = symbol_to_opcode[[opcodeL, opcodeR][addr_ofs]]
                return instruction_info[opcode].opcode + (addr << 8)

        for info in instruction_info.values():
            m = info.alias_pattern.match(instr) or info.pattern.match(instr)
            if m:
                if m.groups():
                    try:
                        val = toint(m[1])
                    except ValueError:
                        val = self.symbol_table[m[1]][0]
                    return info.opcode + (val << 8)
                else:
                    return info.opcode
        else:
            raise SyntaxError(instr)

    def asm_to_mc(self, code):
        if len(code) % 2:
            code = code + ["SKIP"]
        encoded = [self._encode(instr) for instr in code]
        return [(a + (b << 20)) for a, b in pairs(encoded)]

    def _parse(self, lines, second_pass=False):
        section = None
        translated = {}
        pos, ofs = 0, False

        for line in lines:
            # sections
            if line in ['.text', '.data']:
                section = line
                pos, ofs = 0, False
                continue

            # alignment directives
            if line == '.alignl':
                if ofs:
                    if second_pass:
                        translated[pos] += (0xAA << 20)
                    pos += 1
                    ofs = False
                continue
            elif line == '.alignr':
                if not ofs:
                    if second_pass:
                        translated[pos] = 0xAA
                    ofs = True
                continue

            # labels
            m = re.match(r"^(\w+):\s*(.*)", line)
            if m:
                if not second_pass:
                    self.symbol_table[m[1]] = (pos, ofs)
                # stop parsing if nothing left on line
                if not m[2]:
                    continue
                line = m[2]

            # encoding
            if section == '.text':
                if ofs:
                    if second_pass:
                        translated[pos] += self._encode(line) << 20
                    pos += 1
                else:
                    if second_pass:
                        translated[pos] = self._encode(line)
                ofs = not ofs

            elif section == '.data':
                if line.startswith('='):
                    pos = toint(line[1:])
                    continue
                if second_pass:
                    translated[pos] = _parse_mem(line)
                pos += 1

        return translated

    def parse_asm(self, code):
        self.symbol_table = {}

        lines = []
        for line in get_lines(code):
            parts = line.split("&")
            # single instructions
            if len(parts) == 1:
                lines.append(line.strip())
                continue

            # paired instructions
            for part in parts:
                part = part.strip()
                # Automatically replace empty instructions with SKIP
                if len(part) > 0:
                    lines.append(part.strip())
                else:
                    lines.append("SKIP")

        # first pass - build symbol table
        self._parse(lines)
        # second pass - translate
        translated = self._parse(lines, True)

        return translated
