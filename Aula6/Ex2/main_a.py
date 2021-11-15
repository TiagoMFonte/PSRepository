#!/usr/bin/env python
import cv2

def main():
    # initial setup
    capture = cv2.VideoCapture(0)
    window_name = 'A5-Ex2'
    cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)
    while True:
        _, image = capture.read()  # get an image from the camera

        # add code to show acquired image
        cv2.imshow(window_name, image)
        # add code to wait for a key press
        cv2.waitKey(20)

if __name__ == '__main__':
    main()