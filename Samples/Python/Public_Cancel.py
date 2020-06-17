
import requests, time
import hmac
import hashlib
import json

from Common import copper_router_url, publicAPIKey, privateAPIKey

path='/cancel'
url = copper_router_url + ':8080' + path

# Order ID to cancel
jsonData={'id':13045019729921}

timestampMicroseconds = int(round(time.time() * 1000000))

messageToSign = str(timestampMicroseconds) + 'POST' + path + json.dumps(jsonData)
sig = hmac.new(
    str(privateAPIKey),
    msg=messageToSign,
    digestmod=hashlib.sha256
).hexdigest()

headers = {'Authorization': publicAPIKey, 'X-Timestamp':str(timestampMicroseconds), 'X-Signature':sig}

print "POSTing to " + url

r = requests.post(url, json=jsonData, headers=headers) 

print r.text
