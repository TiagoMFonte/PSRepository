#!/usr/bin/python3

def addComplex(x, y):

    a = x[0]
    b = x[1]
    c = y[0]
    d = y[1]

    return(a + c, b + d)

def multiplyComplex(x, y):

    a = x[0]
    b = x[1]
    c = y[0]
    d = y[1]
    result_real = a*c-b*d
    result_im = a*d + b*c
    return (result_real, result_im)

def printComplex(x, prefix=''):

    r = x[0]
    i = x[1]
    print(prefix + str(r) + '+' + str(i) + 'i')

def main():

    c1 = (5, 3)
    c2 = (-2, 7)

    printComplex(c1, prefix = 'c1 = ')

    c3 = addComplex(c1, c2)
    printComplex(c3, prefix= 'Addition = ')

    printComplex(multiplyComplex(c1, c2), prefix = 'Multiplication = ')

if __name__ == '__main__':
    main()