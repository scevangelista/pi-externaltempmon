# Import the Libraries
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import smtplib
import socket

# Vars of control
alerta = 0
alertado = 0

# GPIO of Sensor
sensor_gpío = 25

#Model of Sensor
sensor_model = Adafruit_DHT.DHT11

# Frequency of test
frequency = 10


# Function of send email 
def enviaEmail(message, subject_email):  
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
    humidity, temperature = Adafruit_DHT.read_retry(sensor_model, sensor_gpío);

    if temperature is not None:
        x = int(temperature)
        
        if x < 20:
            print("Temperatura Normal")
            texto = "Estamos com %i graus no Datacenter de Goioere, o uso do ar pode estar elevado." % x;      
            assunto = "MONITORAMENTO DE TEMPERATURA - TEMPERATURA ABAIXO DO NORMAL" 
            alerta = 1
        elif x >= 20 and x < 24:
            print("Temperatura Aceitavel")
            texto = "Agora estamos com %i graus no Datacenter de Goioere, uma temperatura excelente." % x; 
            assunto = "MONITORAMENTO DE TEMPERATURA - TEMPERATURA NORMAL"           
            alerta = 2
        elif x >= 24 and x < 26:
            print("Temperatura fora do Normal")
            texto = "Estamos com %i graus no Datacenter de Goioere, uma temperatura fora do normal." % x;
            assunto = "MONITORAMENTO DE TEMPERATURA - TEMPERATURA FORA DO NORMAL"
            alerta = 3
        elif x >= 26:
            print("Corre!")
            texto = "PROBLEMAS NO AR CONDICIONADO!. Estamos com %i graus no Datacenter de Goioere, uma temperatura MUITO ALTA." % x;
            assunto = "MONITORAMENTO DE TEMPERATURA - PROBLEMAS NO AR CONDICIONADO"
            alerta = 4
        else:
            print("Falha na leitura")

        if alerta != alertado:
            enviaEmail(texto, assunto);
            alertado = alerta
        elif alerta == 4:
            enviaEmail(texto, assunto);

        time.sleep(frequency)
    else:
        # Mensagem de erro de comunicacao com o sensor
        print("Falha ao ler dados do Sensor !!!")
