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
#Filename
file = input("What file would you like to send?")+ ".dat"

if sys == ("Darwin"):
	# Data capture ios #
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
else:
        # Data capture android #
        import androidhelper
        import time
        from datetime import datetime
        import pickle 
        import os
        os.chdir('/storage/emulated/0/acc.data/data_recorded')
# Initialise
        droid = androidhelper.Android()
        dt = 100  # Sets min. time between measurements
        X = []
        Y = []
        Z = []
        t = []

# Record acceleration data (2 = accel)
        droid.startSensingTimed(2, dt)  # Selects sensor
        print('**** Recording ****')
        count = 0
        N = 100
        for i in range(0 , N):
    # Read x, y and z accel.
            x = droid.sensorsReadAccelerometer().result[0]
            y = droid.sensorsReadAccelerometer().result[1]
            z = droid.sensorsReadAccelerometer().result[2]   
        
    # Store accelerations and time
            X.append(x)
            Y.append(y)
            Z.append(z)
            t.append(datetime.now().strftime("%H:%M:%S.%f"))
            
    # Sometimes print time and iteration 
            count += 1
            if count == 10:
                print('Iteration', (i+1), 'of', N)
                print('Time:', datetime.now().strftime("%H:%M:%S.%f"))
                count = 0
    
    # Pause before taking next measurement
            time.sleep(dt/1000.0) 

# Stop recording    
        droid.stopSensing()
        print('**** Finished ****')

# Save time history data
        file = open('data.data','wb')
        my_tuple = tuple((X, Y, Z, t))
        pickle.dump(my_tuple, file)
        
######## Emailing #########
        
msg = MIMEMultipart()
msg['From']= input("what's your email?")
msg['To'] = input("Whom do you wish to email?")
msg['Subject'] = "You got mail!"
msg.preamble = "TEST"
password = input("what is your password?")
part = MIMEBase('application', "ocetot-stream")
part.set_payload(open(file, "rb").read())
encoders.encode_base64(part)
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





