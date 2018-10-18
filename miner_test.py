import hashlib
#import transaction
from flask import Flask, request, jsonify, make_response
import sys, getopt
import requests
import json


app = Flask(__name__)
transactions = [{'receiver': 'mary', 'amount': 2000}, {'receiver': 'anders', 'amount': 200},
                     {'receiver': 'mary', 'amount': 3000}]  # list of all transactions that we have sent


@app.route('/')
def test():
    return 'Hello World'

@app.route('/gettransproof')#, methods=['POST', 'GET'])
def getTransProof():
    answer = {'found': False, 'proof': None, 'root:': None}
    r = request.get_json()
    print(r)
    if r in transactions:
        print('Found a matching transaction')
        print(r)
        answer['found'] = True
    print(r)
    #print('In trans proof')
    #response = {'greeting':'Hello'}
    return jsonify(answer)
    #t = request.json
    #print(t)

app.run(port=5003)
