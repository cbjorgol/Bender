

from BrickPi import *

BrickPiSetup()  										# setup the serial port for communication
############################################
# !  Set the sensor type on the line below.  
BrickPi.SensorType[PORT_1] = TYPE_SENSOR_TOUCH   	#Set the type of sensor at PORT_1.  NXT Touch Sensor.
BrickPi.SensorType[PORT_2] = TYPE_SENSOR_EV3_TOUCH_0  	#Set the type of sensor at PORT_2.  EV3 Touch sensor.
BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B
BrickPi.MotorEnable[PORT_C] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_D] = 1 #Enable the Motor B



def run_forward(speed=200, seconds=3):
    print "Running Forward"
    BrickPi.MotorSpeed[PORT_A] = speed  #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_B] = speed  #Set the speed of MotorB (-255 to 255)
    BrickPi.MotorSpeed[PORT_C] = speed  #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_D] = speed  #Set the speed of MotorB (-255 to 255)

    ot = time.time()
    while(time.time() - ot < seconds):    #running while loop for 3 seconds
        BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
	time.sleep(.001)

if __name__ == '__main__':
    run_forward(60, 0.5)
    run_forward(-60, 0.5)
    run_forward(60, 0.5)
    run_forward(-60, 0.5)
