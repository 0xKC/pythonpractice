import subprocess
import smtplib
import time
from email.mime.text import MIMEText
import android
droid = android.Android()

savedIpAddress = '0.0.0.0'
toAddress = 'Your@email.com'
fromAddress = 'Your@email.com'

pswd = 'Passw0rd'

hourInSeconds = 60 * 60

def findAndCompareIpAddresses():
	currentIpAddress = subprocess.check_output('wget http://ipinfo.io/ip -qO -', shell=True)
	if (currentIpAddress != savedIpAddress):
		sendEmail(currentIpAddress)

def sendEmail(newIpAddress):
	# Create Message
	msg = MIMEText('Raspbery PI Public IP Address has changed. New IP Address = ' + newIpAddress)
	msg['Subject'] = 'IP Address has changed'
	msg['To'] = toAddress
	msg['From'] = fromAddress

	# Connect to google smtp
	s = smtplib.SMTP()
	s.connect('smtp.gmail.com', 587)
	s.starttls()
	s.login(fromAddress, pswd)

	# Send the message
	s.sendmail(fromAddress, toAddress, msg.as_string())
	s.quit()

# Run program indefinitely
while (True):
	findAndCompareIpAddresses()
	time.sleep(hourInSeconds)
