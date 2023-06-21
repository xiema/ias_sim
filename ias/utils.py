from itertools import islice

pow2 = []
k = 1
for _ in range(41):
    pow2.append(k)
    k *= 2


def binstr(n, width, reverse=False):
    "returns the padded 2's complement binary string representation of an int"
    while n < 0:
        n = n + pow2[width]
    bs = format(n, f"0{width}b")
    return bs[-1::-1] if reverse else bs


def binslice(n, width, first=None, last=None):
    """"
    returns the int value of a slice of the binary representation of an int
    """
    if first is None:
        first = 0
    if last is None:
        last = width - 1

    n %= pow2[width]
    first %= width
    last %= width

    return (n % pow2[last+1]) // pow2[first]


def binsplice(n, m, width, first=None, last=None):
    """
    returns the int value after splicing in the bits of m into a position in n
    extra trailing bits from m are discarded
    """
    if first is None:
        first = 0
    if last is None:
        last = width - 1

    n %= pow2[width]
    m %= pow2[last-first+1]
    first %= width
    last %= width

    return (n % pow2[first]) + (m * pow2[first]) + (n // pow2[last+1] * pow2[last+1])


def pairs(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    return zip(islice(iterable, 0, None, 2), islice(iterable, 1, None, 2))


def toint(s):
    "handles int conversion from binary, hex and decimal strings"
    if s.startswith('0b'):
        return int(s, 2)
    if s.startswith('0x'):
        return int(s, 16)
    return int(s)
