# # import the necessary packages
from __future__ import print_function
import sys
import time
from BrickPi import *
import numpy as np
sys.path.append('..')
# import cv2
#
# # load the image and convert it to grayscale
# image = cv2.imread("/home/pi/Bender/jurassic_world.jpg",0)
# #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Original", image)
#
# # initialize the AKAZE descriptor, then detect keypoints and extract
# # local invariant descriptors from the image
# detector = cv2.AKAZE_create()
# (kps, descs) = detector.detectAndCompute(image, None)
# print("keypoints: {}, descriptors: {}".format(len(kps), descs.shape))
#
# # draw the keypoints and show the output image
# cv2.drawKeypoints(image, kps, image, (0, 255, 0))
# cv2.imshow("Output", image)
# cv2.waitKey(0)

# This website explains how to install cv2
# http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/


# import the necessary packages
# from __future__ import print_function
import cv2
from BrickPi import *
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);

# faceCascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



BrickPiSetup()
BrickPi.MotorEnable[PORT_B] = 1  # Enable the Motor B
BrickPi.MotorEnable[PORT_C] = 1  # Enable the Motor A

def update_bender():
    while True:
        BrickPiUpdateValues()
        time.sleep(0.01)

def set_motor_speed(direction, max_speed, min_speed):

    # Ranges from -1 to 1
    direction_centered = direction#(direction - 0.5)*2
    speed_range = max_speed - min_speed
    speed_left  = min_speed + direction_centered * speed_range
    speed_right = min_speed + (1-direction_centered) * speed_range

    print("Speed Left: {0} Speed Right: {1} Direction: {2}".format(speed_left, speed_right, direction))
    BrickPi.MotorSpeed[PORT_B] = int(speed_left)
    BrickPi.MotorSpeed[PORT_C] = int(speed_right)


#in this way it always works, because your get the right "size"
# size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
#         int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# fourcc = cv2.cv.FOURCC('8', 'B', 'P', 'S')     #works, large

# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# out = cv2.VideoWriter('output.avi', fourcc, 2., size, True)

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# cv2.CV_FOURCC('m', 'p', '4', 'v')
#
#
#
#
# out = cv2.VideoWriter('output.mp4', fourcc, 3.0, (640,480))

import thread
thread.start_new_thread(update_bender,())
buffer_time = 10
average_length = 4


t0 = time.time()
face_loc_hist = []
time_of_last_face = time.time()

while(cap.isOpened()):


    # Capture frame-by-frame
    ret, image = cap.read()


    if ret==True:
        # set_motor_speed(1, 20, 1)

        height, width, channels = image.shape
        # Our operations on the frame come here
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (faces, weights) = hog.detectMultiScale(gray, winStride=(4, 4),
                                                padding=(8, 8), scale=1.05)

        # # draw the original bounding boxes
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #



        # faces = faceCascade.detectMultiScale(
        #     gray,
        #     scaleFactor=5.5,
        #     minNeighbors=2,
        #     minSize=(3, 3),
        #     flags = cv2.CASCADE_SCALE_IMAGE
        # )
        faces_exist = len(faces) > 0

        # # Draw a rectangle around the faces
        if faces_exist:
            time_of_last_face = time.time()
            face_locs = []
            for i, (x, y, w, h) in enumerate(faces):

                face_location =  (x + w /2.)/ float(width)
                face_locs.append(face_location)


            face_loc_hist.append(np.mean(face_locs)) # Take mean x location


            #print(face_locs)
            # cv2.rectangle(image, (x, 0), (x+w, 0+h), (0, 255, 0), 2)

            #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                #
                # y = y - 3
                # elapsed = time.time() - t0
                # cv2.putText(image,
                #             "Person "+str(i),
                #             (x, y),
                #             cv2.FONT_HERSHEY_SIMPLEX, 2.2, (0, 0, 255),
                #             thickness=5)

            # time_adjustment = (5 - min(time_since_face, 5)) / 5.
            weighted_to_mean = np.mean(face_loc_hist) #* time_adjustment + 0.5 * 1 - time_adjustment
            set_motor_speed(weighted_to_mean, 250, 80)

        else:
            time_since_face = time.time() - time_of_last_face

            # set_motor_speed(0.5, 80, 80)
            time_adjustment = (buffer_time - min(time_since_face, buffer_time)) / float(buffer_time)
            print(time_adjustment)
            weighted_to_mean = np.mean(face_loc_hist) * time_adjustment + 0.5 * (1 - time_adjustment)
            set_motor_speed(weighted_to_mean, 250, 80)

        if face_loc_hist > average_length:
            face_loc_hist = face_loc_hist[1:]

        print("histarray",face_loc_hist)
        #BrickPiUpdateValues()

        # Display the resulting frame
        # cv2.imshow('frame',image)
        # out.write(image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture

# cap.release()
# out.release()
# out = None
# cv2.destroyAllWindows()

