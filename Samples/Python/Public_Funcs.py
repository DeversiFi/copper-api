#!/usr/bin/python

import sys
import requests, time
import hmac
import hashlib
import json

from Common import copper_router_url, publicAPIKey, privateAPIKey

timestampMicroseconds = int(round(time.time() * 1000000))

def PlaceOrder(market, price, amount):
    path='/place'
    url = copper_router_url + ':8080' + path
    jsonData={'uid':1, 'symbol':market, 'price':float(price), 'amount':float(amount), 'flags':0}
    
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
    
def CancelOrder(orderID):
    path='/cancel'
    url = copper_router_url + ':8080' + path
    jsonData={'id':int(orderID)}
    
    messageToSign = str(timestampMicroseconds) + 'POST' + path + json.dumps(jsonData)
    
    sig = hmac.new(
        str(privateAPIKey),
        msg=messageToSign,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    headers = {'Authorization': publicAPIKey, 'X-Timestamp':str(timestampMicroseconds), 'X-Signature':sig}
    print "POST-ing to " + url
    r = requests.post(url, json=jsonData, headers=headers) 
    print r.text
    
def GetOrders():
    path='/allorders'
    url = copper_router_url + ':8080' + path
    messageToSign = str(timestampMicroseconds) + 'GET' + path
    
    sig = hmac.new(
        str(privateAPIKey),
        msg=messageToSign,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    headers = {'Authorization': publicAPIKey, 'X-Timestamp':str(timestampMicroseconds), 'X-Signature':sig}
    print "GET-ing from " + url
    r = requests.get(url, headers=headers) 
    print r.text
    
def help():
    print "Public_Func.py [mode] {params..}"
    print ""
    print "    PLACE {market} {price} {amount}"
    print "    e.g. PLACE BTCUST 1000.0 10.0"
    print ""
    print "    CANCEL {orderID}"
    print "    e.g. CANCEL 1234567890"
    print ""
    print "    ORDERS"
    print ""

def main(argv):
    if len(argv) < 1:
        help()
        return

    if(argv[0] == 'PLACE' and len(argv) == 4):
        PlaceOrder(argv[1] , argv[2] , argv[3])
    elif(argv[0] == 'CANCEL' and len(argv) == 2): 
        CancelOrder(argv[1])
    elif(argv[0] == 'ORDERS'):
        GetOrders()
    else:
        help()

if __name__ == "__main__":
   main(sys.argv[1:])