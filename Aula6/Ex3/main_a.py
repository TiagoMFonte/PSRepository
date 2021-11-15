#!/usr/bin/env python
import copy
import cv2
import numpy as np

def main():
    # initial setup
    #capture = cv2.VideoCapture(0) #setup video capture for webcam
    capture = cv2.VideoCapture('video_teste.mp4') #setip video capture from video file

    #configure opencv window
    window_name = 'A5-Ex3'
    cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)

    #-----------------------------------------------------------------------------
    #Execute
    #-----------------------------------------------------------------------------

    #Load the cascade
    #Path to classifier
    path_to_classifier = '/home/tiago/bin/opencv-4.5.4/data/haarcascades/'
    face_cascade = cv2.CascadeClassifier(path_to_classifier + 'haarcascade_frontalface_default.xml')


    while True:
        _, image = capture.read() # get an image from the camera
        if image is None:
            print('Video is over, terminating.')
            break #video is over

        height, width,_ = image.shape
        image_gui = copy.deepcopy(image)

        #------------------------------------------------------------------
        #Face Detection
        #------------------------------------------------------------------

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
        faces = face_cascade.detectMultiScale(image_gray, 1.1, 4) #Detect the faces

        for (x, y, w, h) in faces: #Draw the rectangle around each face
            cv2.rectangle(image_gui, (x, y), (x + w, y + h), (255, 0, 0), 2)

            mask_face = np.ndarray((height,width), dtype=np.int8) #create a mask same size as image all zeros
            mask_face.fill(0)
            mask_face = cv2.rectangle(mask_face, (x, y), (x + w, y + h), 255, -1) #draw blue rectangle around face
            cv2.add(image, (-10, 50, -10, 0), dst=image_gui, mask=mask_face) #make mask green


        cv2.imshow(window_name, image_gui)
        cv2.imshow('mask_face', mask_face)

        key = cv2.waitKey(20)

        if key == ord('q'):
            print('You pressed q... terminating.')
            break




if __name__ == '__main__':
    main()