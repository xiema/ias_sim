from .utils import *


class Memory:
    """
    A dict- or list- like container for 'Memory Cells'. Instances can be
    indexed like dicts or lists to directly access or modify the values
    stored in the cells (e.g REG['AC'], MEM[128] = 1). Additionally,
    cells with string keys can be accessed like attributes (e.g. REG.AC,
    REG.PC).
    For int indices, slicing returns a list of values stored in cells
    within the sliced range. Slicing can also be directly applied on the
    bit values in memory cells by slicing with tuples.
       MEM[1844, 0:7] -> the lower 8 bits of the cell at index 1844
       MEM[20, -12:] -> the upper 8 bits of cell 20
       MEM[12, :3, 13, :3] -> first 4 bits in cells 12 and 13
       MEM[[5, 9, 13]] -> full int values in cells 5, 9 and 13

    Note however that ending indices are INCLUSIVE unlike in regular Python.
    This was to be consistent with the written specifications for IAS.
    """

    def __init__(self):
        # need to use original __setattr__ method as this class overrides it
        object.__setattr__(self, 'cells', {})

    def addcell(self, id, bitwidth):
        "create and add MemoryCells accessible by an id key"
        self.cells[id] = MemoryCell(bitwidth)

    def reset(self):
        "zero all MemoryCells"
        for k in self.cells:
            self.cells[k].setvalue(0)

    # ----- INTERNALS -----

    def __getattr__(self, name):
        # attribute access for named elements (like registers)

        if name == 'cells':
            # to make the 'cells' dict visible externally
            return object.__getattr__(self, 'cells')
        if name in self.cells:
            return self.__getitem__(name)
        return self.__getattribute__(name)
        # raise AttributeError

    def __setattr__(self, name, value):
        if name in self.cells:
            self.__setitem__(name, value)
        # else:
        #     raise AttributeError

    def __getitem__(self, key):
        # index access

        # indexing by id, return value in cell
        if type(key) == int or type(key) == str:
            return self.cells[key].getvalue()

        # indexing by slice, return values of range of cells
        if type(key) == slice:
            begin = key.start or 0
            end = key.stop or len(self.cells)
            step = key.step or 1
            return [self.cells[i].getvalue() for i in range(begin, end+1, step)]

        # indexing by tuple
        if type(key) == tuple:
            ret = []
            # expect alternating id-slice pairs
            for id, slic in pairs(key):
                ret.append(self.cells[id].getvalue(slic.start, slic.stop))
            # for 1-item list, return first value
            return ret[0] if len(ret) == 1 else ret

        # indexing by list, get value of each item in list
        if type(key) == list:
            return [self.__getitem__(k) for k in key]

    def __setitem__(self, key, value):
        # similar with __getitem__

        # single
        if type(key) == int or type(key) == str:
            self.cells[key].setvalue(value)

        # slice
        if type(key) == slice:
            start = key.start or 0
            stop = min(key.stop or len(self.cells), start + len(value) - 1)
            for i in range(start, stop + 1, key.step or 1):
                self.cells[i].setvalue(value[i])

        # slice bits
        if type(key) == tuple:
            for id, slic in pairs(key):
                self.cells[id].setvalue(value, slic.start, slic.stop)

        # list
        if type(key) == list:
            for k, v in zip(key, value):
                self.cells[k].setvalue(v)

    def __repr__(self):
        return str(self.cells)


class MemoryCell:
    """
    Generic memory unit. Don't instantiate or manipulate these directly.
    """

    def __init__(self, bitwidth):
        self.data = 0
        self.bitwidth = bitwidth
        self.uprbound = pow2[bitwidth]

    def getvalue(self, start=None, stop=None):
        if start or stop:
            # slice of bits
            return binslice(self.data, self.bitwidth, start, stop)
        else:
            # whole value
            return self.data

    def setvalue(self, value, start=None, stop=None):
        if start or stop:
            # slice of bits
            self.data = binsplice(self.data, value, self.bitwidth, start, stop)
        else:
            # overflow
            # if value >= self.uprbound:
            #     pass
            self.data = value % self.uprbound

    def __repr__(self):
        return binstr(self.data, self.bitwidth)
