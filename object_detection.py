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

import subprocess
import os
import signal

def set_motor_speed(toggle_on, speed, diff):
    BrickPi.MotorSpeed[PORT_B] = toggle_on * speed * diff
    BrickPi.MotorSpeed[PORT_A] = toggle_on * speed
    BrickPiUpdateValues()


if __name__ == '__main__':

    os.setpgrp()
    try:
        BrickPiSetup()
        # BrickPi.SensorType[PORT_2] = TYPE_SENSOR_TOUCH
        BrickPi.SensorType[PORT_1] = TYPE_SENSOR_ULTRASONIC_CONT

        BrickPi.MotorEnable[PORT_B] = 1  # Enable the Motor B
        BrickPi.MotorEnable[PORT_A] = 1  # Enable the Motor A
        BrickPiSetupSensors()

        # BrickPi.Timeout=50000
        # BrickPiSetTimeout()
        #
        # speed = 120
        #
        # button_vals = np.array([])
        # toggle_on = True
        # t0 = time.time()
        #
        # min_stream_len = sys.argv[1] if len(sys.argv) > 1 else 4

        while True:

            print BrickPi.Sensor[PORT_1]
            #
            # set_motor_speed(toggle_on, speed, 2)
            # # print 'motors should be running now'
            #
            # touch = BrickPi.Sensor[PORT_2]
            #
            # button_vals = np.append(button_vals, touch)
            #
            # if len(sys.argv) < 2:
            #     min_stream_len = 35
            # else:
            #     min_stream_len = int(sys.argv[1])
            #
            # if len(button_vals) > min_stream_len:
            #     button_vals = button_vals[1:]
            #
            # # print button_vals
            # if min(button_vals) == 1 and len(button_vals) >= min_stream_len:
            #     toggle_on = not toggle_on
            #     set_motor_speed(toggle_on, speed, 2)
            #     button_vals = np.array([])
            #     for i in range(100):
            #         BrickPiUpdateValues()
            #         time.sleep(0.015)

                    # infrared = BrickPi.Sensor[PORT_1]
                    # button_value = interpret_response(infrared)
                    # button_vals = np.append(button_vals, button_value)
                    # if len(button_vals) > 3:
                    #     button_vals = button_vals[1:]

                    # print button_vals, infrared

                    # On / Off switch for speed
                    # if np.all(button_vals == 9):
                    #    on = 1 - on

            # BrickPiUpdateValues()
            time.sleep(.001)
    except:
        assert 1 == 2

    finally:
        os.killpg(0, signal.SIGKILL)
