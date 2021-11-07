#!/usr/bin/python3
import time
import colorama
import cv2

def main():

    image_filename = '../images/atlas2000_e_atlasmv.png'
    image = cv2.imread(image_filename, cv2.IMREAD_COLOR) # Load an image
    cv2.imshow('window', image)  # Display the image

    image_bright = image + 20  # aumenta o brilho da imagem
    cv2.imshow('window2', image_bright)

    cv2.waitKey(0) # wait for a key press before proceeding


if __name__ == '__main__':
    main()