#Imports needed packages
import requests
import json
import time
import dbWorker
from resources import constants

def weatherStation():

    #Creates a request object and attaches the api secret key as a header
    headers = {'X-Api-Secret': constants.apiSecret}
    r = requests.get(f"https://api.weatherlink.com/v2/historic/{constants.stationID}?api-key={constants.apiKey}&start-timestamp={int(time.time()-905)}&end-timestamp={int(time.time())-5}", headers=headers)

    #Loads the json into a dictionary in python
    r = json.loads(r.text)
    
    #We will only need the path below so I am setting the 'r' variable to the path to make life easier
    r = r['sensors'][0]['data'][0]

    #Takes the info from the the JSON dictionary and commits it to the database

    dbWorker.insertData((r.get('wind_speed_avg'), r.get('uv_dose'), r.get('wind_speed_hi'),r.get('wind_dir_of_hi'), r.get('wind_chill'), r.get('solar_rad_hi'), r.get('deg_days_heat'),r.get('thw_index'), r.get('bar'), r.get('hum_out'), r.get('tz_offset'), r.get('uv_index_hi'),r.get('temp_out'), r.get('temp_out_lo'), r.get('wet_bulb'), r.get('temp_out_hi'), r.get('solar_rad_avg'),r.get('bar_alt'), r.get('arch_int'), r.get('wind_run'), r.get('solar_energy'), r.get('dew_point_out'),r.get('rain_rate_hi_clicks'), r.get('wind_dir_of_prevail'), r.get('et'), r.get('air_density'),r.get('rainfall_in'), r.get('heat_index_out'), r.get('thsw_index'), r.get('rainfall_mm'),r.get('night_cloud_cover'), r.get('deg_days_cool'), r.get('rain_rate_hi_in'), r.get('uv_index_avg'),r.get('wind_num_samples'), r.get('emc'), r.get('rain_rate_hi_mm'), r.get('rev_type'),r.get('rainfall_clicks'), r.get('ts'), r.get('abs_press')), 'weatherlink')

if __name__ == '__main__':
    weatherStation()