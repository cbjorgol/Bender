#!/usr/bin/python
'''
    Author: Igor Maculan - n3wtron@gmail.com
    A Simple mjpg stream http server
'''
import cv2
import Image
import thread
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time
capture=None
import numpy as np

from imutils.object_detection import non_max_suppression

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    rc,img = capture.read()
                    if not rc:
                        continue

                    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    (rects, weights) = hog.detectMultiScale(gray, winStride=(4, 4),
                                                            padding=(8, 8), scale=1.05)

                    # draw the original bounding boxes
                    for (x, y, w, h) in rects:
                        cv2.rectangle(imgRGB, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    # apply non-maxima suppression to the bounding boxes using a
                    # fairly large overlap threshold to try to maintain overlapping
                    # boxes that are still people
                    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
                    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)


                    # draw the final bounding boxes
                    for (xA, yA, xB, yB) in pick:
                        cv2.rectangle(imgRGB, (xA, yA), (xB, yB), (0, 255, 0), 2)


                    # (kps, descs) = detector.detectAndCompute(imgRGB, None)
                    # print("keypoints: {}, descriptors: {}".format(len(kps), descs.shape))
                    #
                    # draw the keypoints and show the output image
                    # cv2.drawKeypoints(imgRGB, kps, imgRGB, (0, 255, 0))

                    # Adding face detection code
                    # height, width, channels = img.shape
                    # faces = faceCascade.detectMultiScale(
                    #     gray,
                    #     scaleFactor=1.1,
                    #     minNeighbors=5,
                    #     minSize=(10, 10),
                    #     flags=cv2.CASCADE_SCALE_IMAGE
                    # )
                    # faces_exist = len(faces) > 0
                    # if faces_exist:
                    #     for i, (x, y, w, h) in enumerate(faces):
                    #         cv2.rectangle(imgRGB, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    jpg = Image.fromarray(imgRGB)
                    tmpFile = StringIO.StringIO()
                    jpg.save(tmpFile,'JPEG')
                    self.wfile.write("--jpgboundary")
                    self.send_header('Content-type','image/jpeg')
                    self.send_header('Content-length',str(tmpFile.len))
                    self.end_headers()
                    jpg.save(self.wfile,'JPEG')
                    time.sleep(0.05)
                except KeyboardInterrupt:
                    break
            return
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://10.0.0.244/:8084/cam.mjpg"/>')
            self.wfile.write('</body></html>')
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""



def main():
    global faceCascade
    faceCascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

    global detector
    detector = cv2.AKAZE_create()

    global capture
    capture = cv2.VideoCapture(0)

    global hog
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320);
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240);
    capture.set(cv2.CAP_PROP_SATURATION, 0.2);
    global img
    try:
        server = ThreadedHTTPServer(('10.0.0.244', 8084), CamHandler)
        print "server started"
        server.serve_forever()
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()

if __name__ == '__main__':
    main()