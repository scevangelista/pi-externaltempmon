# Import the Libraries
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import smtplib
import socket

# Vars of control
alert = 0
alerted = 0

# GPIO of Sensor
sensor_gpio = 25

#Model of Sensor
sensor_model = Adafruit_DHT.DHT11

# Frequency of test
frequency = 10


# Function of send email 
def sendEmail(message, subject_email):  
    # Configure the emails #
    from_email = 'fromemail@...'
    from_password = 'password'
    from_smtp = 'smtp...'
    to_email = 'destination@...'

    msg = '\r\n'.join([
        'From: %s' % from_email,
        'To: %s' % to_email,
        'Subject: %s' % subject_email,
        '',
        '%s' % message
    ])
    
    smtp = smtplib.SMTP(from_smtp, 587)
    smtp.starttls()
    smtp.login(from_email, from_password)
    smtp.sendmail(from_email, to_email, msg)
    smtp.quit()
    return 1
 


GPIO.setmode(GPIO.BOARD)

while(1):
    humidity, temperature = Adafruit_DHT.read_retry(sensor_model, sensor_gpio);

    if temperature is not None:
        x = int(temperature)
        
        if x < 20:
            print("Low temperature")
            body = "%i degrees Celsius in Datacenter." % x;      
            subject = "TEMPERATURE MONITOR - LOW" 
            alert = 1
        elif x >= 20 and x < 24:
            print("Normal temperatura")
            body = "%i degrees Celsius in Datacenter." % x; 
            subject = "TEMPERATURE MONITOR - NORMAL"           
            alert = 2
        elif x >= 24 and x < 26:
            print("High Temperature")
            body = "%i degrees Celsius in Datacenter." % x;
            subject = "TEMPERATURE MONITOR - HIGH - WARNING"
            alert = 3
        elif x >= 26:
            print("Very High Temperature")
            body = "Air conditioning problems! %i degrees Celsius in Datacenter." % x;
            subject = "TEMPERATURE MONITOR - VERY HIGH - ALERT"
            alert = 4
        else:
            print("Error in DHT")

        if alert != alerted:
            sendEmail(body, subject);
            alerted = alert
        elif alert == 4:
            sendEmail(body, subject);

        time.sleep(frequency)
    else:
        print("Error to retrieve sensor data");
