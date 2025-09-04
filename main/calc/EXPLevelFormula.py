import numpy


def minEXP(level: int):
    return numpy.ceil(numpy.divide(numpy.power(1.2, level)-1.2, 0.012))

def EXPtoLevel(exp: int):
    return numpy.trunc(numpy.divide(numpy.log(numpy.multiply(0.012, exp) + 1.2),numpy.log(1.2)))