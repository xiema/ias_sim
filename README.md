# IAS Simulator

A simple computer simulator that uses the IAS instruction set, programmed in Python.

# Input Program Language

## Memory Map

Direct mapping of the initial memory for the computer. Each line represents the contents of the memory at a specific address. The memory contents are specified as either one or four numbers, each of which may be in decimal, binary or hexadecimal format. Example of contents are:

    01 100 05 200

    0b10 0x1A 0b101 0x1B

    5000

Optionally, an address can be specified for the following memory content. The address can be specified at the start of the line, or in the previous line:

    0x12 0b101 0xF 0b101 0x1
    
    =0x12
    0b101 0xF 0b101 0x1

If the address for a line is omitted, the line is understood to be the memory location after the one addressed in the previous line. Memory contents do not have to be in order. Memory locations that are not explicitly defined are left untouched.

Line comments can also be added with the `#` symbol.

## IAS Assembly

IAS instructions translated in a more readable format.

An assembly source program (.asm) is divided into two sections specified by the keywords `.text` and `.data`. `.text` can contain assembler instructions, while `.data` may only contain constants, similar to the memory map format.

The following instructions are available:

| Syntax            | Description
| ----------------- | -----------
| LOAD MQ           | Transfer AC to MQ
| LOAD MQ,M(X)      | Transfer M(X) to MQ
| STOR M(X)         | Transfer AC to M(X)
| LOAD M(X)         | Transfer M(X) to AC
| LOAD -M(X)        | Transfer -M(X) to AC
| LOAD \|M(X)\|     | Transfer absolute value of M(X) to AC
| LOAD -\|M(X)\|    | Transfer negative absolute value of M(X) to AC
| JUMP M(X,0:19)    | Take next instruction from left half of M(X)
| JUMP M(X,20:39)   | Take next instruction from right half of M(X)
| JUMP + M(X,0:19)  | If AC is nonnegative, take next instruction from left half of M(X)
| JUMP + M(X,20:39) | If AC is nonnegative, take next instruction from right half of M(X)
| ADD M(X)          | Add M(X) to AC and store in AC
| ADD \|M(X)\|      | Add absolute value of M(X) to AC and store in AC
| SUB M(X)          | Subtract M(X) from AC and store in AC
| SUB \|M(X)\|      | Subtract absolute value of M(X) and store in AC
| MUL M(X)          | Multiply M(X) by MQ, store most significant bits in AC and least significant bits in MQ
| DIV M(X)          | Divide AC by M(X), store quotient in MQ and remainder in AC
| LSH               | Left shift AC by 1 bit
| RSH               | Right shift AC by 1 bit
| STOR M(X,8:19)    | Replace left address field at M(X) by 12 rightmost bits of AC
| STOR M(X,28:39)   | Replace right address field at M(X) by 12 rightmost bits of AC
| EXIT              | End execution

For any instruction with an address field `X`, the `X` must be replaced by a binary, decimal or hexadecimal number reprenting a valid memory address.

# Usage

Can launch with a memory map:

    # in repo folder
    python -m ias -m memmap.txt

Or launch with an assembler file:

    python -m ias -a code.asm

Add `--dump` to dump the memory contents to stdout

    python -m ias -a code.asm --dump

# To Do

- [x] Load from memory map
- [x] Translate assembly <-> machine code
- [ ] Add assembler shorthand/pseudoinstructions, directives
