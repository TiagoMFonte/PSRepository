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
    image_bgr = cv2.imread(args['image1'], cv2.IMREAD_COLOR)
    image_b, image_g, image_r = cv2.split(image_bgr)

    #process image
    _, image_b_processed = cv2.threshold(image_b, 50, 255, cv2.THRESH_BINARY)
    _, image_g_processed = cv2.threshold(image_g, 100, 255, cv2.THRESH_BINARY)
    _, image_r_processed = cv2.threshold(image_r, 150, 255, cv2.THRESH_BINARY)

    new_image_bgr = cv2.merge((image_b_processed, image_g_processed, image_r_processed))

    #visualization
    cv2.imshow('original', image_bgr)
    cv2.imshow('processed b', image_b_processed)
    cv2.imshow('processed g', image_g_processed)
    cv2.imshow('processed r', image_r_processed)
    cv2.imshow('new_image_bgr', new_image_bgr)


    cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == '__main__':
    main()