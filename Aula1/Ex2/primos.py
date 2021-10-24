#!/usr/bin/python3
from colorama import Fore, Back, Style

maximum_number = 10

def isPrime(value):
    print('\nReference number ' + str(value))

    for i in range(2, value):
        remainder = value % i
        print(str(value) + '/' + str(i) + ' has remainder ' + str(remainder))
        if remainder == 0:
            return False
    return True

def main():
    print("Starting to compute prime numbers up to " + str(maximum_number))
    counter = 0
    for i in range(1, maximum_number):
        if isPrime(i):
            print(Back.YELLOW + Fore.BLUE + Style.DIM + 'Number ' + Back.GREEN + Fore.RED +
                  Style.DIM + str(i) + Back.YELLOW + Fore.BLUE + Style.DIM + ' is prime.' + Style.RESET_ALL)
            counter += 1
        else:
            print('Number ' + str(i) + ' is not prime.')
    print(Fore.BLUE + 'We have ' + str(counter) + ' prime numbers.' + Style.RESET_ALL)

if __name__ == "__main__":
    main()