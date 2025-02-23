I have all of these scripts running on a raspberry pi 3.

I have them scheduled to run use crontab. 
The weatherStation.py script runs every 5 minutes, the dailyAvgs.py runs once a day at 5:59 AM, and the send email runs once a day at 6 AM.

This is all publuc data collected using a WeatherLink weather station. The weather stations are made by Davis Intstruments.
This project was created due to not being able to see a 24 hour spread of data between two days. 
You could only see 12 am to 12 pm, we needed 6:30 am to 6:30 am.