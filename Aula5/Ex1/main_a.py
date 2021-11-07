#!/usr/bin/python3
import argparse
import numpy as np
import time
import colorama
import cv2


def main():
    #choose image
    parser = argparse.ArgumentParser(description='Opencv example.')
    parser.add_argument('--image1', type=str, help='Path to image')
    args = vars(parser.parse_args())


    # Load an image
    image_original = cv2.imread(args['image1'], cv2.IMREAD_COLOR)
    image_gray = cv2.cvtColor(image_original, cv2.COLOR_BGR2GRAY)

    #process image
    retval, image_processed = cv2.threshold(image_gray, 128, 255, cv2.THRESH_BINARY)

    #visualization
    cv2.imshow('original', image_original)
    cv2.imshow('processed', image_processed)
    cv2.imshow('gray', image_gray)
    cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == '__main__':
    main()