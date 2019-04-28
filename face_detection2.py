# # import the necessary packages
from __future__ import print_function
import sys
import time
from BrickPi import *
import numpy as np
import thread
import cv2
import subprocess

from imutils.object_detection import non_max_suppression

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 680);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);

face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

t0 = time.time()
time_since_update = 9999
while(cap.isOpened()):
    ret, image = cap.read()

    if ret==True:
        re_colored=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        faces = face_cascade.detectMultiScale(re_colored, 1.22, 2, flags = cv2.CASCADE_SCALE_IMAGE)
        print("Humans Actively Monitored:", len(faces))
        for (x,y,w,h) in faces:
            cv2.rectangle(re_colored,(x,y),(x+w,y+h),(255,255,0), 2)

        
        def command():
            return subprocess.Popen(['python', 'chuck_norris_jokes.py'])

        if len(faces) > 1:
            time_since_update = time.time() - t0
            if time_since_update > 60:
                t0 = time.time()
                command()
            
                        
        # Display the resulting frame
        cv2.imshow('frame', re_colored)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
out = None
cv2.destroyAllWindows()
