import requests
import json
import constants

headers = {'X-Api-Secret': constants.apiSecret}
r = requests.get(f"https://api.weatherlink.com/v2/stations?api-key={constants.apiKey}", headers=headers)
r = json.loads(r.text)
for i in range(len(r['stations'])):
    print(r['stations'][i],'\n\n')