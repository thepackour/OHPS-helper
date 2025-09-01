import numpy


def minEXP(level: int):
    return int(numpy.ceil(numpy.divide(numpy.power(1.2, level)-1.2, 0.012)))