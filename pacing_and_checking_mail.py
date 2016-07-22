import imaplib
import email
import time
from speak import speak
from chuck_norris_jokes import say_chuck_norris_joke
from cat_facts import say_cat_fact
from robot_keys import account, password
from weather import get_weather
from BrickPi import *
import numpy as np
import sys


def interpret_response(response_in):
	# Check for error reading.  If it's an error reading, return 0.
	if response_in < 4278190080:

		#print response_in
		if response_in < 4278190336 and response_in >=  16777216:
			response_in = response_in / 16777216
			if response_in <= 9:
				return response_in
			else:
				#print "Failure! "
				return -5
		
		elif response_in < 16777216 and response_in >=  65536:
			response_in = response_in / 65536
			if response_in <= 9:
				return response_in
			else:
				#print "Failure!"
				return -5
		elif response_in < 65536 and response_in >=  256:
			response_in = response_in / 256
			if response_in <= 9:
				return response_in
			else:
				#print "Failure!"
				return -5
		elif response_in < 256 and response_in >=  0:
				return response_in		
		else:
			return response_in
		
	else:
		return -3

def interpret_button(number):
	if number == 0:
		print "Nothing pressed!"
	elif number == 9:
		print "Top button pressed!"
	elif number == 1:
		print "Top red button pressed!"
	elif number == 2:
		print "Bottom red button pressed!"
	elif number == 3:
		print "Top blue button pressed!"
	elif number == 4:
		print "Bottom blue button pressed!"
	else:
		print "Something else was pressed!"
		

if __name__ == '__main__':

    import subprocess
    import os
    import signal

    os.setpgrp()
    try:

        mail_status = subprocess.Popen(['python','mail.py'])

        BrickPiSetup()
        BrickPi.SensorType[PORT_2] = TYPE_SENSOR_EV3_TOUCH_0

        BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B
        BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
        BrickPiSetupSensors()

        BrickPi.Timeout=50000
        BrickPiSetTimeout()

        speed = 150

        button_vals = np.array([])
        toggle_on = False
        t0 = time.time()


        min_stream_len = sys.argv[1] if len(sys.argv) > 1 else 4

        while True:

            BrickPi.MotorSpeed[PORT_B] = toggle_on * speed * 2
            BrickPi.MotorSpeed[PORT_A] = toggle_on * speed
            BrickPiUpdateValues()

            #button_vals = np.append(button_vals, touch)

            #if len(sys.argv) < 2:
                #    min_stream_len = 3
                #else:
                #    min_stream_len = int(sys.argv[1])

                #if len(button_vals) > min_stream_len:
                #    button_vals = button_vals[1:]

            #if min(button_vals) >= 1010 and len(button_vals) >= min_stream_len:
                #    toggle_on = not toggle_on
            #    button_vals = np.array([])

                # infrared = BrickPi.Sensor[PORT_1]
                # button_value = interpret_response(infrared)
                # button_vals = np.append(button_vals, button_value)
                #if len(button_vals) > 3:
                #     button_vals = button_vals[1:]

                # print button_vals, infrared

                # On / Off switch for speed
                # if np.all(button_vals == 9):
                #    on = 1 - on


            BrickPiUpdateValues()
            time.sleep(.05)

    finally:
        os.killpg(0, signal.SIGKILL)
