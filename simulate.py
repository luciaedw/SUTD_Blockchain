import time
import requests
import json
from flask import jsonify

"""Dictionaries to be sent with requests"""
newTrans= {'receiver':None, 'amount':None, 'message':None}


spvs = [5003] #port numbers of spv-clients
miners = [5000, 5001]#, 5001, 5002]#port numbers of miners
loops = 1 #we're going to run each spv for t seconds and y loops
t = 0.1 #how many seconds each time block is
j = 0
t_end = time.time() + t

"""Start by sending public key to all neighbours"""
for port in (miners + spvs):
    url = 'http://127.0.0.1:' + str(port) + '/tellneighbours'
    requests.get(url)

#while time.time() < t_end:
#for i in range(loops):
#    print('Loop: ' + str(i))
for port in miners:
    url = 'http://127.0.0.1:' + str(port) + '/mine'
    r = requests.get(url)
    print(r.text)
    url = 'http://127.0.0.1:' + str(port) + '/newtrans'
    print(port)
    data = newTrans.copy()
    data['receiver'] = ''
    data['amount'] = 10
    data['message']= 'Sending some coin'
    r = requests.post(url, json=data)
    print(r.text)

#print(j)


newTrans= {'receiver':None, 'amount':None, 'message':None}