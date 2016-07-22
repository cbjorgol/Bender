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

class mailmanager():
    def __init__(self, account, password):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(account, password)

    def check_mail(self):

        self.mail.list()
        self.mail.select('inbox')

        n = 0
        (retcode, messages) = self.mail.search(None, '(UNSEEN)')
        if retcode == 'OK':

            for num in messages[0].split():
                print 'Processing '
                n = n + 1
                typ, data = self.mail.fetch(num, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        original = email.message_from_string(response_part[1])

                        print original['From'], "Subject: ", original['Subject']
                        print get_payload(original)
                        typ, data = self.mail.store(num, '+FLAGS', '\\Seen')

        if n == 0:
            return None
        else:
            return original

def get_payload(original):
    """
    This needs to be able to handle payloads
      when multiple emails come through

    Parameters
    ----------
    original

    Returns
    -------

    """
    # TODO: Set up multiple email handling
    if len(original) > 1:
        payload = original.get_payload()
    else:
        payload = original.get_payload()
    print payload
    return payload


def check_mail(mail):
    mail_contents = mail.check_mail()
    if mail_contents is not None:
        if mail_contents['Subject'] is None:
            speak(mail_contents.get_payload())

        elif 'Subject' in mail_contents:

            chuck_norris_request = mail_contents['Subject'].lower().find('chuck norris') != -1
            cat_fact_request = mail_contents['Subject'].lower().find('cat fact') != -1
            weather_request = mail_contents['Subject'].lower().find('weather') != -1

            if chuck_norris_request:
                say_chuck_norris_joke()
            elif cat_fact_request:
                say_cat_fact()
            elif weather_request:
                get_weather()
            else:
                speak(get_payload(mail_contents))
    else:
        print "no facts found"



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

    BrickPiSetup()  
    # BrickPi.SensorType[PORT_1] = TYPE_SENSOR_EV3_INFRARED_M2
    BrickPi.SensorType[PORT_2] = TYPE_SENSOR_EV3_TOUCH_0 # TYPE_SENSOR_TOUCH 

    BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B
    BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
    BrickPiSetupSensors()

    BrickPi.Timeout=50000
    BrickPiSetTimeout()
    # BrickPiSetupSensors()  

    mail = mailmanager(account, password)
    mail_wait = 20
    speed = 150

    button_vals = np.array([])
    toggle_on = False
    t0 = time.time()
    time_since_mail = 10

   
    min_stream_len = sys.argv[1] if len(sys.argv) > 1 else 4
    
    while True:
        
        BrickPi.MotorSpeed[PORT_B] = toggle_on * speed * 2
	BrickPi.MotorSpeed[PORT_A] = toggle_on * speed
	BrickPiUpdateValues()
	
        time_since_mail = time.time() - t0
        if time_since_mail > mail_wait:
            check_mail(mail)
            time_since_mail = mail_wait
            t0 = time.time()

        touch = BrickPi.Sensor[PORT_2]
 
  	touch = 0 if touch is None else touch        

	button_vals = np.append(button_vals, touch)

	if len(sys.argv) < 2:
            min_stream_len = 3
        else:
            min_stream_len = int(sys.argv[1])
            
        if len(button_vals) > min_stream_len:
            button_vals = button_vals[1:]
        
        print button_vals, toggle_on

	if np.min(button_vals) >= 1010 and len(button_vals) >= min_stream_len:
            toggle_on = not toggle_on
	    button_vals = np.array([])

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
