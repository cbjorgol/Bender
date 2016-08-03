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
import io

import subprocess
import os
import signal

def set_motor_speed(toggle_on, speed, diff):
    BrickPi.MotorSpeed[PORT_B] = toggle_on * speed * diff
    BrickPi.MotorSpeed[PORT_A] = toggle_on * speed
    BrickPiUpdateValues()


if __name__ == '__main__':



    BrickPiSetup()  # setup the serial port for communication
    port_number = PORT_1	# Define the port number here.  

    BrickPi.SensorType[port_number] = TYPE_SENSOR_ULTRASONIC_CONT   #Set the type of sensor at PORT_1
    BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

    with io.open('spam.txt', 'w') as file:
        while True:
            result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors 
            if not result :
                file.write(unicode(BrickPi.Sensor[port_number])+u',\n')     #BrickPi.Sensor[PORT] stores the value obtained from sensor
            time.sleep(.01)     # sleep for 10 ms
    

