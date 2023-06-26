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

# Usage

Can launch with a memory map:

    python -m ias memmap.txt

# To Do

[x] Load from memory map
[ ] Translate assembly <-> binary

