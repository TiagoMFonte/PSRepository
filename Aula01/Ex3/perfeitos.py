#!/usr/bin/python3

from colorama import Fore, Back, Style
maximum_number = 10

def getDividers(value):
    print('\nReference number ' + str(value))
    dividers = []

    for i in range(1, value):
        remainder = value % i
        print(str(value) + '/' + str(i) + ' has remainder ' + str(remainder))
        if remainder == 0:
            dividers.append(i)
    print('Dividers for referenced number ' + str(value) + ' is ' + str(dividers))
    return dividers

def isPerfect(value):

    dividers = getDividers(value)
    sum_of_dividers = sum(dividers)
    if sum_of_dividers == value:
        return True
    return False


def main():
    print("Starting to compute perfect numbers up to " + str(maximum_number))
    counter = 0
    for i in range(1, maximum_number):
        if isPerfect(i):
            print(Fore.BLUE + 'Number ' + str(i) + ' is perfect.' + Style.RESET_ALL)
            counter += 1
        else:
            print('Number ' + str(i) + ' is not perfect.')
    print('The number of perfect numbers is ' + str(counter))


if __name__ == "__main__":
    main()