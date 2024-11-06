import requests
import json

headers = {'X-Api-Secret': 'API_SECRET'}
r = requests.get("https://api.weatherlink.com/v2/stations?api-key=API_KEY", headers=headers)
r = json.loads(r.text)
for i in range(len(r['stations'])):
    print(r['stations'][i],'\n\n')