#!/usr/bin/python3
import argparse
import copy

import numpy as np
import time
import colorama
import cv2

# Global variables
window_name = 'window - Ex3a'
image_gray = None


def onTrackbarMin(minimum):
    global image_gray
    mask_black = cv2.inRange(image_gray, 0, minimum)
    mask_black = ~mask_black
    mask_black = mask_black.astype(np.bool)
    image_gray_tmp = copy.copy(image_gray)
    image_gray_tmp[mask_black] = 0
    cv2.imshow(window_name, image_gray_tmp)

def onTrackbarMax(maximum):
    global image_gray
    mask_black = cv2.inRange(image_gray, maximum, 255)
    mask_black = ~mask_black
    mask_black = mask_black.astype(np.bool)
    image_gray_tmp = copy.copy(image_gray)
    image_gray_tmp[mask_black] = 255
    cv2.imshow(window_name, image_gray_tmp)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', type=str, required=True,help='Full path to image file.')
    args = vars(parser.parse_args())

    image = cv2.imread(args['image'], cv2.IMREAD_COLOR)  # Load an image
    global image_gray # use global var
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert bgr to gray image (single channel)
    cv2.namedWindow(window_name)

    cv2.createTrackbar('Minimum', window_name, 0, 255, onTrackbarMin)
    cv2.createTrackbar('Maximum', window_name, 0, 255, onTrackbarMax)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()