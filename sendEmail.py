#Imports packages for later use
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
import os
import dbWorker
from resources import constants
import time

confPath = constants.configPath

sender = constants.email
password = constants.password
config = configparser.ConfigParser(allow_no_value=True)
emails = {}
emailsReceive = {}
toSend = {}
configValuesExplained = {'day': 'The day the data was collected/organized.', 'curtemp': 'The latest temerature from the Weather Station.', 'hitemp': 'The highest temperature in the last 24 hours.', 'lotemp': 'The lowest Temperature in the last 24 hours.', 'totalrain24': 'The total rainfall for the last 24 hours, in inches.'}

def getHigh(list: list, position: int):
    high = 0
    for item in list:
        if item[position] > high:
            high = item[position]
    return high

def getLow(list: list, position: int):
    low = 0
    for item in list:
        if item[position] > low:
            low = item[position]
    return low

def writeFile():
    config.write(open(confPath, 'w'))

def createConfig():
    config['Emails'] = {'e1': 'DEFAULT EMAIL'}
    config['Email Receives'] = {'e1': 'DEFAULT DATA'}
    config['Instructions'] = {}
    config.set('Instructions', '; Below are all the values that you can use to retreive data.')
    config.set('Instructions', '; The values are followed by a line explaining what they do.\n')
    for key, value in configValuesExplained.items():
        config.set('Instructions', f'; {key}')
        config.set('Instructions', f'; {value}\n')
    writeFile()

def configReader():
    if not os.path.exists(confPath):
        createConfig()
    else:
        config.read(confPath)


def emailProcesser():
    for key, value in config['Emails'].items():
        valuesNP = value.split(',')
        valuesP = []
        for item in valuesNP:
            item = item.strip()
            valuesP.append(item)
        emails[key] = valuesP
    for key, value in config['Email Receives'].items():
        valuesNP = value.split(',')
        valuesP = []
        for item in valuesNP:
            item = item.strip()
            valuesP.append(item)
        emailsReceive[key] = valuesP

def sendMorningMail():
    
    for key, email_list in emails.items():
        for email in email_list:  # Loop over individual emails in email_list
            
            # Process columns only once per email
            columns = emailsReceive[key]  # Get columns specific to this email
            weatherlink = dbWorker.getValues(int(time.time()), int(time.time()) - (24*60*60), 'weatherlink', columns)

            highTemp = getHigh(weatherlink, 0)
            lowTemp = getLow(weatherlink, 0)
            currentTemp = weatherlink[-1][0]
            totalRain = 0
            for item in weatherlink:
                totalRain += int(item[1])

            body = f'''
            24 Hour Data:
            Total Rain: {totalRain} in
            Highest Temperature: {highTemp} F
            Lowest Temperature: {lowTemp} F
            Current Temperature: {currentTemp} F'''

            msg = MIMEMultipart()
            msg.attach(MIMEText(str(body)))
            msg['subject'] = 'WeatherLink Data'
            msg['from'] = sender
            msg['to'] = email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                s.login(sender, password)
                s.sendmail(sender, email, msg.as_string())

if __name__ == '__main__':
    configReader()
    emailProcesser()
    sendMorningMail()
