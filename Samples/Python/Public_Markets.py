
import requests, time
import hmac
import hashlib
import json

from Common import copper_router_url, publicAPIKey, privateAPIKey

path='/markets'
url = copper_router_url + ':8080' + path

timestampMicroseconds = int(round(time.time() * 1000000))

messageToSign = str(timestampMicroseconds) + 'GET' + path 
sig = hmac.new(
    str(privateAPIKey),
    msg=messageToSign,
    digestmod=hashlib.sha256
).hexdigest()

headers = {'Authorization': publicAPIKey, 'X-Timestamp':str(timestampMicroseconds), 'X-Signature':sig}

print "GETting from " + url

r = requests.get(url,  headers=headers) 

print r.text
