from BrickPi import *
import time

BrickPiSetup()  										# setup the serial port for communication
############################################
# !  Set the sensor type on the line below.  



BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B
BrickPi.MotorEnable[PORT_C] = 1 #Enable the Motor A



def move(speed=200, right_speed=None, seconds=3):

    if right_speed==None:
        right_speed = speed

    BrickPi.MotorSpeed[PORT_B] = speed  #Set the speed of MotorB (-255 to 255)
    BrickPi.MotorSpeed[PORT_C] = right_speed  #Set the speed of MotorA (-255 to 255)

    ot = time.time()
    while(time.time() - ot < seconds):    #running while loop for 3 seconds
        BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
    time.sleep(.001)



if __name__ == '__main__':
    move(60, 20,  seconds=0.8)
