#!/usr/bin/python

import sys
import requests, time
import hmac
import hashlib
import json

from Common import copper_router_url, publicAPIKey, privateAPIKey

timestampMicroseconds = int(round(time.time() * 1000000))

def GenerateSignature(data):
    return hmac.new(bytes(privateAPIKey, 'latin-1'), bytes(data,'latin-1'), hashlib.sha256).hexdigest()

def PlaceOrder(market, price, amount):
    path='/place'
    url = copper_router_url + ':8080' + path
    jsonData={'uid':1, 'symbol':market, 'price':float(price), 'amount':float(amount), 'flags':0}
    
    messageToSign = str(timestampMicroseconds) + 'POST' + path + json.dumps(jsonData)
    sig = GenerateSignature(messageToSign)
    
    headers = {'Authorization': publicAPIKey, 'X-Timestamp':str(timestampMicroseconds), 'X-Signature':sig}
    print ("POSTing to " + url)
    r = requests.post(url, json=jsonData, headers=headers) 
    print (r.text)
    
def CancelOrder(orderID):
    path='/cancel'
    url = copper_router_url + ':8080' + path
    jsonData={'id':int(orderID)}
    
    messageToSign = str(timestampMicroseconds) + 'POST' + path + json.dumps(jsonData)    
    sig = GenerateSignature(messageToSign)
    
    headers = {'Authorization': publicAPIKey, 'X-Timestamp':str(timestampMicroseconds), 'X-Signature':sig}
    print ("POST-ing to " + url)
    r = requests.post(url, json=jsonData, headers=headers) 
    print (r.text)
    
def GetOrders():
    path='/openorders'
    url = copper_router_url + ':8080' + path

    messageToSign = str(timestampMicroseconds) + 'GET' + path
    sig = GenerateSignature(messageToSign)

    headers = {'Authorization': publicAPIKey, 'X-Timestamp':str(timestampMicroseconds), 'X-Signature':sig}
    print ("GET-ing from " + url)
    r = requests.get(url, headers=headers) 
    print ("Raw:")
    print (r.text)
    print ("")
    resultObj = json.loads(r.text)
    if(resultObj[1] == "OK"):
        for order in resultObj[2]:
            print("oid: " + str(order[0]) + " state: " + order[5] + " market: " + order[2] + " price: " + str(order[3]) + " amount: " + str(order[4]))
    
def GetAllOrders():
    path='/allorders'
    url = copper_router_url + ':8080' + path

    messageToSign = str(timestampMicroseconds) + 'GET' + path
    sig = GenerateSignature(messageToSign)
    
    headers = {'Authorization': publicAPIKey, 'X-Timestamp':str(timestampMicroseconds), 'X-Signature':sig}
    print ("GET-ing from " + url)
    r = requests.get(url, headers=headers) 
    print ("Raw:")
    print (r.text)
    print ("")
    resultObj = json.loads(r.text)
    if(resultObj[1] == "OK"):
        for order in resultObj[2]:
            print("oid: " + order[0] + " state:" + order[7] + " tsPlaced:" + str(order[1]) + " price:" + str(order[4]) + " amount:" + str(order[5]))

def GetBalances():
    path='/balances'
    url = copper_router_url + ':8080' + path

    messageToSign = str(timestampMicroseconds) + 'GET' + path
    sig = GenerateSignature(messageToSign)
    
    headers = {'Authorization': publicAPIKey, 'X-Timestamp':str(timestampMicroseconds), 'X-Signature':sig}
    print ("GET-ing from " + url)
    r = requests.get(url, headers=headers) 
    print ("Raw:")
    print (r.text)
    print ("")
    resultObj = json.loads(r.text)
    if(resultObj[1] == "OK"):
        for balance in resultObj[2]:
            print(balance[0] + " " + str(balance[1]) + " (reserved:" + str(balance[2]) + ")")
    
def help():
    print ("Public_Func.py [mode] {params..}")
    print ("")
    print ("    PLACE {market} {price} {amount}")
    print ("    e.g. PLACE BTCUST 1000.0 10.0")
    print ("")
    print ("    CANCEL {orderID}")
    print ("    e.g. CANCEL 1234567890")
    print ("")
    print ("    ORDERS")
    print ("")
    print ("    ALLORDERS")
    print ("")
    print ("    BALANCES")
    print ("")

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
    elif(argv[0] == 'ALLORDERS'):
        GetAllOrders()
    elif(argv[0] == 'BALANCES'):
        GetBalances()
    else:
        help()

if __name__ == "__main__":
   main(sys.argv[1:])