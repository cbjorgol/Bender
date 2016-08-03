import subprocess
import os
import signal
import numpy as np

from BrickPi import *


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

def set_motor_speed(toggle_on, speed, diff):
    BrickPi.MotorSpeed[PORT_B] = toggle_on * speed * diff
    BrickPi.MotorSpeed[PORT_A] = toggle_on * speed
    BrickPiUpdateValues()
		

if __name__ == '__main__':


    os.setpgrp()
    try:
       assert 1 == 2
    except:

        # np=str(raw_input())
        # print np
        mail_status = subprocess.Popen(['python','mail.py'])

        BrickPiSetup()
        BrickPi.SensorType[PORT_2] = TYPE_SENSOR_TOUCH

        BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B
        BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
        BrickPiSetupSensors()

        # BrickPi.Timeout=50000
        # BrickPiSetTimeout()

        speed = 120

        button_vals = np.array([])
        toggle_on = True
        t0 = time.time()


        min_stream_len = sys.argv[1] if len(sys.argv) > 1 else 4

        while True:
            
            set_motor_speed(toggle_on, speed, 2)

            touch = BrickPi.Sensor[PORT_2]            
            
            button_vals = np.append(button_vals, touch)   
            
            if len(sys.argv) < 2:
                min_stream_len = 35
            else:
                min_stream_len = int(sys.argv[1])

            if len(button_vals) > min_stream_len:
                button_vals = button_vals[1:]

            # print button_vals
            if min(button_vals) == 1 and len(button_vals) >= min_stream_len:
                toggle_on = not toggle_on
                set_motor_speed(toggle_on, speed, 2)
                button_vals = np.array([])
                for i in range(100):
                    BrickPiUpdateValues()
                    time.sleep(0.015)

            #BrickPiUpdateValues()
            time.sleep(.001)

    finally:
        os.killpg(0, signal.SIGKILL)
