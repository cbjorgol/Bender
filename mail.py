import urllib
import time
import imaplib
import email
import sys
import traceback
import smtplib
import os
from datetime import datetime
import ConfigParser
import email
import email.mime.application
from email.mime.image import MIMEImage 
from email.mime.text import MIMEText

class Mailmanager():
	def __init__(self, login, password) :
		self.login = login
		self.password = password

		self.mail = imaplib.IMAP4_SSL('imap.gmail.com', 587)
		self.mail.login(login, password)

	def getMail(self) :
		self.mail.list()
		status, msgs = self.mail.select()
		if status == 'OK' :
			result, data = self.mail.uid('search', None, "(UNSEEN)")    
			if data[0] != '':            
				time.sleep(.1)
				latest_email_uid = data[0].split()[-1]
				result, data = self.mail.uid('fetch', latest_email_uid, '(RFC822)')
				raw_email = data[0][1]   
				message = email.message_from_string(raw_email)
				name, sender = self.get_sender(message)
				subj = email.utils.parseaddr(message['Subject'])[1]
				text = self.getBody(message) 
				return name, sender, subj, text
			
			else :
				return 0,0,0,0
		else :
			raise mailError('Bad status from server')

	def stop(self) :
		self.mail.close()
		self.mail.logout()        
		
		
	def sendEmail(self, recipient, subject, message) :           
		smtpserver = smtplib.SMTP("smtp.gmail.com",587)
		smtpserver.ehlo()
		smtpserver.starttls()
			
		smtpserver.ehlo
		smtpserver.login(login, password)
		log("Constructing Message")
		msg = email.MIMEMultipart.MIMEMultipart('mixed')	
			
		msg['From'] = login
		msg['To'] = recipient
		msg['Subject'] = subject
		
		#msgText = MIMEText('<b>%s</b><br><img src="cid:"' + config.pictureName + '"><br>' % message, 'html')   
		msg.attach(MIMEText(message))   # Added, and edited the previous line
		
		try :
			numList = sender.split('.')
			number = numList[ 1]
			assert int(number)
			log("From text message, MMS not supported.  No picture sent")
									
		except :  
			try :
				attachment = config.tempDirectory + '/' + config.pictureName
				fp = open(attachment, 'rb')   
				log("Reading attachement")                                                 
				img = MIMEImage(fp.read())
				fp.close()
				log("Attaching message")
				msg.attach(img)
				
			except Exception, detail :
				log('Error attaching image: ' + str(detail))
		#header = 'To:' + recipient + '\n' + 'From: ' + login + '\n' + 'Subject: ' + subject+ ' \n'
		#msg = header + '\n '+ message + '\n\n'   
		log("Sending message")
		smtpserver.sendmail(login, recipient, msg.as_string())
		smtpserver.quit()
		log("Done senMailmanagerding message")
		#os.system("rm " + attachment)
		

	def get_sender(self,email_message) :
		sender = email.utils.parseaddr(email_message['From'])    
		name = sender[0]
		addr = sender[1]
		return name, addr

	def getBody(self, email_message_instance):
		maintype = email_message_instance.get_content_maintype()
		if maintype == 'multipart':
			for part in email_message_instance.get_payload():
				if part.get_content_maintype() == 'text':
					return part.get_payload()

		elif maintype == 'text':
			return email_message_instance.get_payload()

if __name__ == '__main__':

    account = 'benderbotmail@gmail.com'
    password = 'cb101682'


    

    import imaplib
    import email
    import time
    from speak import speak
    from chuck_norris_jokes import say_chuck_norris_joke

    class mailmanager():
        def __init__(self, account, password):
            self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
            self.mail.login(account, password)

            
        def check_mail(self):
            try:
                self.mail.list()
                self.mail.select('inbox')
                result, data = self.mail.search(None, "ALL")

                ids = data[0]
                id_list = ids.split()
                latest_email_id = id_list[-1]

                result, data = self.mail.fetch(latest_email_id, "(RFC822)")
                raw_email = data[0][1]

                return raw_email
            except:
                return 'no content'
            
    print email, password
    mail = mailmanager(account, password)

    for i in range(50):
        mail_contents = mail.check_mail()
        
        if mail_contents.lower().find('chuck norris') != -1:
            say_chuck_norris_joke()
        else:
            print "no chuck norris commands found"
        time.sleep(20)
            
            
