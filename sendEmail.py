#Imports packages for later use
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
import os
import sqlite3
from pathlib import Path

dbPath = '/home/pi/Desktop/PatokaProject/resources/month.db'
confPath = '/home/pi/Desktop/PatokaProject/resources/config.ini'

sender = 'SENDER_EMAIL'
config = configparser.ConfigParser(allow_no_value=True)
emails = {}
emailsReceive = {}
toSend = {}
configValuesExplained = {'day': 'The day the data was collected/organized.', 'curtemp': 'The latest temerature from the Weather Station.', 'hitemp': 'The highest temperature in the last 24 hours.', 'lotemp': 'The lowest Temperature in the last 24 hours.', 'totalrain24': 'The total rainfall for the last 24 hours, in inches.'}

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

def sendEmail():
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    
    for key, email_list in emails.items():
        for email in email_list:  # Loop over individual emails in email_list
            body = ''  # Initialize body for each email
            
            # Process columns only once per email
            columns = emailsReceive[key]  # Get columns specific to this email
            for column in columns:
                cur.execute(f'SELECT {column} FROM monthly WHERE day>=(SELECT MAX(day) FROM monthly) LIMIT 1')
                data = cur.fetchall()
                if data:  # Only append if data is not empty
                    body += f"{configValuesExplained[column]}: {data[0][0]}\n"

            if body:  # Only send email if body is not empty
                msg = MIMEMultipart()
                msg.attach(MIMEText(str(body)))
                msg['subject'] = 'WeatherLink Data'
                msg['from'] = sender
                msg['to'] = email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                    s.login(sender, 'SENDER PASSWROD')
                    s.sendmail(sender, email, msg.as_string())
    
    con.close()

if __name__ == '__main__':
    configReader()
    emailProcesser()
    sendEmail()
