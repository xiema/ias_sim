# IAS Simulator

A simple computer simulator that uses the IAS instruction set, programmed in Python.

# Input Program Language

## Memory Snapshot

Direct mapping of the initial memory for the computer. Each line represents the contents of the memory at a specific address. Each line must be in the following format:

    ADDR OP ARG OP ARG
    # ADDR - memory address
    # OP - opcode of instruction
    # ARG - operand/argument for the instruction

The numbers should be in hexadecimal format. Leading zeroes are optional. Line comments can also be added with the `#` symbol.

Memory contents do not have to be in order. Memory locations that are not explicitly defined are left untouched.

### Shorthand

Alternatively, a shorthand can be used for defining a memory snapshot. Addresses, opcodes and operands can be specified in binary, decimal or hexadecimal format. Binary and hexadecimal must be explicitly indicated by prefixing with `0b` and `0x`. Single values can also be used to represent data taking the whole width of the memory location.

Memory address is optional, and can be specified at the start of the line, or in the previous line. If the address for a line is omitted, the line is understood to be the memory location after the one addressed in the previous line.

    # Explicitly set address at 0x12
    0x12 0b101 0xF 0b101 0x1
    # Next line is understood to be 0x13
    0b11 0x1 0x0 0x0
    
    # Can also place the address in the previous line
    =0x12
    0b101 0xF 0b101 0x1

    # Full-width data
    0x10
    12345

## IAS Assembly

IAS instructions translated in a more readable format.

An assembly source program (.asm) is divided into two sections specified by the keywords `.text` and `.data`. `.text` can contain assembler instructions, while `.data` may only contain constants, similar to the snapshot format.

The following instructions are available:

| Syntax   | Original symbol   | Description
| -------- | ----------------- | -----------
| lm       | LOAD MQ           | Transfer MQ to AC
| lam x    | LOAD MQ,M(X)      | Transfer M(X) to MQ
| sa x     | STOR M(X)         | Transfer AC to M(X)
| la x     | LOAD M(X)         | Transfer M(X) to AC
| la -x    | LOAD -M(X)        | Transfer -M(X) to AC
| la \|x   | LOAD \|M(X)\|     | Transfer absolute value of M(X) to AC
| la -\|x  | LOAD -\|M(X)\|    | Transfer negative absolute value of M(X) to AC
| jl x     | JUMP M(X,0:19)    | Take next instruction from left half of M(X)
| jr x     | JUMP M(X,20:39)   | Take next instruction from right half of M(X)
| bl x     | JUMP + M(X,0:19)  | If AC is nonnegative, take next instruction from left half of M(X)
| br x     | JUMP + M(X,20:39) | If AC is nonnegative, take next instruction from right half of M(X)
| add x    | ADD M(X)          | Add M(X) to AC and store in AC
| add \|x  | ADD \|M(X)\|      | Add absolute value of M(X) to AC and store in AC
| sub x    | SUB M(X)          | Subtract M(X) from AC and store in AC
| sub \|x  | SUB \|M(X)\|      | Subtract absolute value of M(X) and store in AC
| muld x   | MUL M(X)          | Multiply M(X) by MQ, store most significant bits in AC and least significant bits in MQ
| divd x   | DIV M(X)          | Divide AC by M(X), store quotient in MQ and remainder in AC
| lsh      | LSH               | Left shift AC by 1 bit
| rsh      | RSH               | Right shift AC by 1 bit
| sal x    | STOR M(X,8:19)    | Replace left address field at M(X) by 12 rightmost bits of AC
| sar x    | STOR M(X,28:39)   | Replace right address field at M(X) by 12 rightmost bits of AC
| exit     | EXIT              | End execution
| skip     | SKIP              | Do nothing

Either the shorthand syntax or the original symbol may be used. For any instruction with an address field `x` (or `X`), the `x` must be replaced by either a number (binary, decimal or hexadecimal) reprenting a valid memory address, or a symbol defined by the `label:` syntax.

Labels can be used to represent memory addresses defined in the code, automatically replaced upon translation:

    .text
    my_label:
    la x1 & add x2
    # do other stuff...
    # then loop back
    jl my_label &

    .data
    x1: 23
    x2: 98

Labels may be composed of alphanumeric characters and underscores.

Since instructions in IAS architecture come in pairs in the memory the `&` keyword can be used to separate at most two instructions in the same line, so that the alignment of instructions can be explicitly shown. If either the left or right side of the `&` are empty, then that side is automatically replaced with a `SKIP` instruction.

Note: when a label is defined on a right-aligned instruction and a `jl` or `bl` instruction is used to jump to it, the label functions the same as if the label were defined on the instruction right before it (the left-aligned instruction on the same memory location).

### Label alignment

Due to the peculiarity of the paired instructions in the IAS architecture, if one wants to address a specific instruction in the program, one needs to know the alignment of the instruction in the memory. To make this easier, the assembler detects the alignments of instructions and can automatically determine the appropriate operation to insert. For example, instead of the `jl` and `jr` operations, one can use the `ja` pseudo-instruction:

    la c1
    add c2
    sa a

    start:  # first instruction is right-aligned
        la x1
        add x2
        # do other stuff...

        # this jumps to `sa a`
        # jl start

        # this correctly jumps to `la x1`
        ja start

        # this correctly jumps to `la x1`, but requires manually managing the instruction alignment
        # jr start

This also works with the `ba` pseudo-instruction for the `bl` and `br` instructions, and the `saa` for `sal` and `sar`. Note that these are not available in the original syntax.

Additionally, one can use the `.alignl` or `.alignr` directives to ensure alignment of the next instruction.


# Usage

Can launch with a memory snapshot, either a direct mapping or in shorthand:

    # in repo folder
    python -m ias -s mem.sn
    # shorthand mode
    python -m ias -s mem_short.sn --shorthand

Or launch with an assembler file:

    python -m ias -a code.asm

Add `--dump` to dump the memory contents to stdout

    python -m ias -a code.asm --dump

# To Do

- [x] Load from memory map
- [x] Translate assembly <-> machine code
- [x] Assembly labels
- [x] Assembly shorthand aliases
- [ ] Assembly pseudoinstructions
- [ ] Assembly directives
- [ ] UI with memory view and stepping
