import time
import requests
import json


"""Gonna try and simulate """
spvs = [5000, 5001,5002] #port numbers of spv-clients
miners = []#port numbers of miners
loops = 2 #we're going to run each spv for t seconds and y loops
t = 0.1 #how many seconds each time block is
j = 0
for i in range(loops):
    print('Loop: ' + str(i))
    for port in spvs:
        url = 'http://127.0.0.1:' + str(port) + '/run'
        print(port)
        t_end = time.time() + t
        while time.time() < t_end:
            #j +=1
            r = requests.get(url)
        print(r.json())

#print(j)


