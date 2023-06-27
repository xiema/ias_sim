import re

from .instruct import instruction_info
from .utils import toint, get_lines, pairs
from .translate import _parse_mem


class Assembler():

    def __init__(self):
        self.symbol_table = {}

    def _encode(self, instr):
        for info in instruction_info.values():
            m = info.pattern.match(instr)
            if m:
                if m.groups():
                    try:
                        val = toint(m[1])
                    except ValueError:
                        val = self.symbol_table[m[1]]
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
            if line in ['.text', '.data']:
                section = line
                pos, ofs = 0, False
                continue

            m = re.match(r"^(\w+):\s*(.*)", line)
            if m:
                if not second_pass:
                    self.symbol_table[m[1]] = pos
                # stop parsing if nothing left on line
                if not m[2]:
                    continue
                line = m[2]

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

        self._parse(lines)
        translated = self._parse(lines, True)

        return translated
