#!/usr/bin/python3

from colorama import Fore, Back, Style

import readchar

def printAllCharsUpTo(stop_char):

    print('I dont know how to do this yet...')
    print('Printing all values up to stop_char ' + str(stop_char))
    for i in range(ord(' '), ord(stop_char)+1):
        print(chr(i))

def readAllUpTo(stop_key):
    count_pressed_numbers = 0
    count_pressed_others = 0

    while True:
        print('Type something (X to stop). ')
        pressed_key = readchar.readkey()
        if str.isnumeric(pressed_key):
            count_pressed_numbers += 1
        else:
            count_pressed_others += 1


        if pressed_key == stop_key:
            print('You typed ' + Fore.RED + Style.BRIGHT + pressed_key + Style.RESET_ALL + '...' + ' terminating.')
            break
        else:
            print('Thank you for typing ' + pressed_key)

    print('You entered ' + str(count_pressed_numbers) + ' numbers.')
    print('You entered ' + str(count_pressed_others) + ' others.')

def main():

    #Ex4a
    #print('Give me the stop char...')
    #pressed_char = readchar.readchar()
    #printAllCharsUpTo(pressed_char)

    #Ex4b
    readAllUpTo('X')


if __name__ == '__main__':
    main()