import motion
from time import sleep
import console
import pickle
import smtplib,ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from smtplib import SMTPException
import platform

sys = platform.system()

if sys == ("Darwin"):
	
	file = input("What file would you like to send?")+ ".dat"

	console.alert('Motion Plot', 'When you tap Continue, accelerometer (motion) data will be recorded for 5 seconds.', 'Continue')
	motion.start_updates()
	sleep(0.2)
	print('Capturing motion data...')
	num_samples = 100
	data = []
	for i in range(num_samples):
		sleep(0.10)
	g = motion.get_gravity()
	data.append(g)
	motion.stop_updates()
	print('Capture finished, plotting...')

	
	
	pickle_out = open(file,"wb")
	pickle.dump(data, pickle_out)
	pickle_out.close()
	
	print("Finished")
########
	msg = MIMEMultipart()
	msg['From']= input("what's your email?")
	msg['To'] = input("Whom do you wish to email?")
	msg['Subject'] = "You got mail!"
	msg.preamble = "TEST"
	password = input("what is your password?")


	part = MIMEBase('application', "ocetot-stream")
#trying shit out
	part.set_payload(open(file, "rb").read())
	encoders.encode_base64(part)
#trying shit out
	part.add_header('Content-Disposition', 'attachment', filename = file)
	msg.attach(part)

	body = input("what do you wish to write to them?")
	msg.attach(MIMEText(body,'html'))

    
	try:
    		s = smtplib.SMTP('smtp.gmail.com', 587)
    		s.ehlo()
    		s.starttls()
    		s.ehlo()
    		s.login(user = msg['From'], password = password)
    		s.sendmail(msg['From'], msg['To'], msg.as_string())
    		s.quit()
	except SMTPException as error:
        		print ("ERROR")





