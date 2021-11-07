#!/usr/bin/python3
import argparse
import numpy as np
import time
import colorama
import cv2


def main():
    #choose image
    parser = argparse.ArgumentParser(description='Opencv example.')
    parser.add_argument('--image1', required=True, type=str, help='Path to image')
    args = vars(parser.parse_args())


    # Load an image
    image_bgr = cv2.imread(args['image1'], cv2.IMREAD_COLOR)
    image_b, image_g, image_r = cv2.split(image_bgr)

    ranges = {'b': {'min':0, 'max':100},
              'g': {'min':88, 'max':256},
              'r': {'min':0, 'max':100}}

   #Processing
    mins = np.array([ranges['b']['min'], ranges['g']['min'], ranges['r']['min']])
    maxs = np.array([ranges['b']['max'], ranges['g']['max'], ranges['r']['max']])
    mask = cv2.inRange(image_bgr, mins, maxs)
    mask = mask.astype(np.bool)

    #image_bgr[np.logical_not(mask)] = (0,0,0)
    image_bgr[np.logical_not(mask)] = image_bgr[np.logical_not(mask)] * 0.5
    image_bgr[mask] = image_bgr[mask] * 1.5
    #New image whick will contain only the copy of the masked pixels


    #visualization
    cv2.imshow('original', image_bgr)
    cv2.imshow('image_processed', mask.astype(np.uint8)+255)


    cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == '__main__':
    main()