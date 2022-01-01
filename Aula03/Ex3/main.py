#!/usr/bin/python3
from collections import namedtuple

Complex = namedtuple('Complex', ['r', 'i'])


def addComplex(x, y):
    a = x.r
    b = x.i
    c = y.r
    d = y.i

    return Complex(r=a + c, i=b + d)

def multiplyComplex(x, y):
    a = x.r
    b = x.i
    c = y.r
    d = y.i
    result_real = a * c - b * d
    result_im = a * d + b * c
    return Complex(result_real, result_im)


def printComplex(x, prefix=''):
    a = x.r
    b = x.i
    print(prefix + str(a) + '+' + str(b) + 'i')


def main():
    # define two complex numbers as tuples of size two
    c1 = Complex(5, 3)  # use order when not naming
    c2 = Complex(i=7, r=-2)  # if items are names order is not relevant
    print('c1 = ' + str(c1)) # named tuple looks nice when printed


    printComplex(c1, prefix='c1 = ')

    c3 = addComplex(c1, c2)
    printComplex(c3, prefix='Addition = ')

    printComplex(multiplyComplex(c1, c2), prefix='Multiplication = ')


if __name__ == '__main__':
    main()