account = 'benderbotmail@gmail.com'
password = 'cb101682'

import imaplib
import email
import time
from speak import speak
from chuck_norris_jokes import say_chuck_norris_joke
from cat_facts import say_cat_fact


class mailmanager():
    def __init__(self, account, password):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(account, password)

    def check_mail(self):

        # self.mail.list()
        # self.mail.select('inbox')
        # result, data = self.mail.search(None, "ALL")
        #
        # ids = data[0]
        # id_list = ids.split()
        # latest_email_id = id_list[-1]
        #
        # result, data = self.mail.fetch(latest_email_id, "(RFC822)")
        # raw_email = data[0][1]
        #
        # return raw_email

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
                        print original.get_payload()
                        typ, data = self.mail.store(num, '+FLAGS', '\\Seen')

        if n == 0:
            return None
        else:
            return original

if __name__ == '__main__':


    mail = mailmanager(account, password)

    for i in range(50):
        mail_contents = mail.check_mail()
        if mail_contents is not None:
            if mail_contents['Subject'] is None:
                speak(mail_contents.get_payload())

            elif 'Subject' in mail_contents:
                chuck_norris_request = mail_contents['Subject'].lower().find('chuck norris') != -1
                cat_fact_request = mail_contents['Subject'].lower().find('cat fact') != -1
                if chuck_norris_request:
                    say_chuck_norris_joke()
                elif cat_fact_request:
                    say_cat_fact()
                else:
                    speak(mail_contents.get_payload())
        else:
            print "no facts found"
        time.sleep(20)