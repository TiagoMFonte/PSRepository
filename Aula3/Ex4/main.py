#!/usr/bin/python3

class Complex:

    def __init__(self, r, i):
        self.r = r  # store real part in class instance
        self.i = i  # store imaginary part in class instance

    def add(self, x):
        a = self.r
        b = self.i
        c = x.r
        d = x.i
        self.r = a + c
        self.i = b + d


    def multiply(self, x):
        a = self.r
        b = self.i
        c = x.r
        d = x.i
        self.r = a * c - b * d
        self.i = a * d + b * c

    def __str__(self):
        a = self.r
        b = self.i
        return str(a) + '+' + str(b) + 'i'

def main():
    c1 = Complex(4, 8)
    c2 = Complex(6, -7)
    print(c1)
    c1.add(c2)
    print(c1)
    c1.multiply(c2)
    print(c1)

if __name__ == '__main__':
    main()