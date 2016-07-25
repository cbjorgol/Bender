import imaplib
import email
import time
from speak import speak
from chuck_norris_jokes import say_chuck_norris_joke
from cat_facts import say_cat_fact
from robot_keys import account, password
from weather import get_weather
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



if __name__ == '__main__':

    mail = mailmanager(account, password)
    mail_wait = 20

    while True:
        check_mail(mail)
        time.sleep(20)
