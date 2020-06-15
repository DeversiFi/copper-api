
import requests, time
import hmac
import hashlib
import json

from Common import copper_router_url, publicAPIKey, privateAPIKey

path='/place'
url = copper_router_url + ':8080' + path

jsonData={'uid':1, 'symbol':'BTCUSD', 'price':10.0, 'amount':1.0, 'flags':0}

timestampMicroseconds = int(round(time.time() * 1000000))

messageToSign = str(timestampMicroseconds) + 'POST' + path + json.dumps(jsonData)
sig = hmac.new(
    str(privateAPIKey),
    msg=messageToSign,
    digestmod=hashlib.sha256
).hexdigest()

headers = {'Authorization': publicAPIKey, 'X-Timestamp':str(timestampMicroseconds), 'X-Signature':sig}

r = requests.post(url, json=jsonData, headers=headers) 

print r.text
