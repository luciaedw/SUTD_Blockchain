import time
import requests
import json


"""Gonna try and simulate """
spvs = [5002] #port numbers of spv-clients
miners = [5000]#, 5001, 5002]#port numbers of miners
loops = 1 #we're going to run each spv for t seconds and y loops
t = 0.1 #how many seconds each time block is
j = 0
t_end = time.time() + t
#while time.time() < t_end:
#for i in range(loops):
#    print('Loop: ' + str(i))
for port in miners:
    url = 'http://127.0.0.1:' + str(port) + '/run'
    print(port)
    r = requests.get(url)
    print(r)

#print(j)

