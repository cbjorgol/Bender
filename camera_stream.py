#!/usr/bin/python
'''
	Author: Igor Maculan - n3wtron@gmail.com
	A Simple mjpg stream http server
'''
import cv2
import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time
capture=None

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print "1"
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

					# Adding face detection code
					gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					height, width, channels = img.shape
					faces = faceCascade.detectMultiScale(
						gray,
						scaleFactor=1.1,
						minNeighbors=5,
						minSize=(10, 10),
						flags=cv2.CASCADE_SCALE_IMAGE
					)
					faces_exist = len(faces) > 0
					if faces_exist:
						for i, (x, y, w, h) in enumerate(faces):
							cv2.rectangle(imgRGB, (x, y), (x + w, y + h), (0, 255, 0), 2)

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
	global capture
	capture = cv2.VideoCapture(0)
	global faceCascade
	faceCascade = cv2.CascadeClassifier('../opencv-3.1.0/data/haarcascades/haarcascade_frontalface_default.xml')

	capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320);
	capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240);
	capture.set(cv2.CAP_PROP_SATURATION,0.2);
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