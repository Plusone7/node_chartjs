import requests
import simplejson as json
url = "https://www.googleapis.com/urlshortener/v1/url"
payload = {"longUrl": "http://www.google.com/"}
header = {"Content-Type":"application/json"}

r = requests.post(url, json=payload , headers = header)
#print(r.text)
print("--------------------------------------------")
#print(r.headers)
print("--------------------------------------------")
#print(json.loads(r.text)["error"]["code"])