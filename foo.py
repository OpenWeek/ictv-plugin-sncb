import urllib.request, urllib.error, urllib.parse
import requests #pip install requests
import json
import time
BASE_URL="http://api.irail.be/"
URLS={
    'stations':'stations',
    'schedules':'connections',
    'liveboard': 'liveboard',
    'vehicle': 'vehicle'
}

DEFAULT_ARGS="?format=json"
head= {'user-agent':'ICTVbooyy/0.69 (ictv.github.con; ictv@4.life)'}
payload = { 'station':'Ottignies', 'arrdep':'departures', 'lang':'nl', 'format':'json', 'alert':'true'}
payloadLLN = { 'station':'Louvain-la-Neuve', 'arrdep':'departures', 'lang':'nl', 'format':'json', 'alert':'true'}

r = requests.get(BASE_URL+'liveboard/',params=payloadLLN, headers=head)


def pretty_print(json_file):
    parsed = json.loads(json_file)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    None


parsed = json.loads(r.text)
for i in parsed["departures"]["departure"]:
    print(i['station'] + ', ' + time.strftime('%H:%M', time.localtime(int(i['time']))) + ', platform : ' + i['platform'])

time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))