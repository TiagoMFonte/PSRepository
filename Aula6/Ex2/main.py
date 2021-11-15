#!/usr/bin/env python
import cv2

def main():
    # initial setup
    #capture = cv2.VideoCapture(0) #stup video capture for webcam
    capture = cv2.VideoCapture('video_teste.mp4') #setup video capture from video files

    #configure opencv window
    window_name = 'A5-Ex2'
    cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)
    while True:
        _, image = capture.read() # get an image from the camera
        if image is None:
            print('Video is over, terminating.')
            break #video is over

        cv2.imshow(window_name, image)
        key = cv2.waitKey(20)

        if key == ord('q'):
            print('You pressed q... terminating.')
            break




    # add code to show acquired image
    # add code to wait for a key press

if __name__ == '__main__':
    main()