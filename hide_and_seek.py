# # import the necessary packages
from __future__ import print_function
import sys
import time
from BrickPi import *
import numpy as np
import thread
import cv2

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);

faceCascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

#hog = cv2.HOGDescriptor()
#hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


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
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# fourcc = cv2.cv.FOURCC('8', 'B', 'P', 'S')     #works, large

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('output.avi', fourcc, 2., size, True)

#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#cv2.CV_FOURCC('m', 'p', '4', 'v')
#out = cv2.VideoWriter('benerview.mp4', fourcc, 3.0, (640,480))



buffer_time = 2
average_length = 5

thread.start_new_thread(update_bender,())


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

        #(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
        #                                        padding=(8, 8), scale=1.1)
        
        faces = faceCascade.detectMultiScale(
             gray,
             scaleFactor=1.2,
             minNeighbors=3,
             minSize=(3, 3),
             flags = cv2.CASCADE_SCALE_IMAGE
        )

        num_objects = len(faces)

        if num_objects > 0:

            object_locs = []
            for i, (x, y, w, h) in enumerate(faces):
                left = x / float(width)
                right = x / float(width)
                w = w / float(width)

                if right < 0.5:
                    object_location = left
                elif left > 0.5:
                    object_location = left + w
                else:
                    object_location = (left + w)/2.


                print(left, right, w,  object_location)

                object_locs.append(object_location)

            # set_motor_speed(np.mean(object_locs), 250, 10)
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

            # def weight_face_hist(face_loc_hist):
            #     arr = np.array(face_loc_hist)
            #     arr[:, 1] = time.time() - arr[:, 1]
            #     weighted_to_mean = np.prod(arr, axis=1) / arr[:, 1] #* time_adjustment + 0.5 * 1 - time_adjustment
            #     print("Weighted_to_mean:",weighted_to_mean, 'arr',arr)
            #     return weighted_to_mean[0]
            #
            # weighted_to_mean = weight_face_hist(face_loc_hist)
            # set_motor_speed(weighted_to_mean, 250, 40)
        else:
            pass
            #set_motor_speed(0.0, 250, 10)
        #     if len(face_loc_hist) == 0:
        #         set_motor_speed(0.5, 250, 40)
        #     else:
        #         weighted_to_mean = weight_face_hist(face_loc_hist)
        #         # set_motor_speed(0.5, 80, 80)
        #         # time_adjustment = (buffer_time - min(time_since_face, buffer_time)) / float(buffer_time)
        #         # print("Time Adj:", time_adjustment)
        #         # weighted_to_mean = np.mean(face_loc_hist) * time_adjustment + 0.5 * (1 - time_adjustment)
        #         set_motor_speed(weighted_to_mean, 250, 80)
        #
        # if len(face_loc_hist) >= average_length:
        #     face_loc_hist = face_loc_hist[1:]

        #BrickPiUpdateValues()

        # Display the resulting frame
        cv2.imshow('frame',image)
        # out.write(image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture

cap.release()
out.release()
out = None
cv2.destroyAllWindows()
