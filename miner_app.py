import hashlib
#import transaction
from flask import Flask, request, jsonify
import sys, getopt
import requests
import json
from blockChain import blockChain
from ecdsa import SigningKey
from binascii import hexlify
from miner import Miner
from block import block

app = Flask(__name__)

testChain = blockChain()
sk = SigningKey.generate() # uses NIST192p
vk = sk.get_verifying_key().to_string()
miner = Miner(sk, hexlify(vk).decode(), testChain)
neighbours = [5000, 5001, 5002]

@app.route('/')
def index():
    return jsonify('Testing')

@app.route('/test2')
def test2():
    return jsonify('Hello World!')

@app.route('/getpubkey')
def getPubKey():
    return jsonify(miner.pubKey)
#
# @app.route('/updateNonce', methods=['GET'])
# def updateNonce():
#     spv_client.updateNonce()
#     return jsonify(spv_client.getNonce())
#
# @app.route('/gettrans/<idx>')#, methods=['POST', 'GET'])
# def getTrans(idx):
#     trans = spv_client.getTransaction(int(idx))
#     return jsonify(trans)
#
# @app.route('/getnodespk')
# def getNodePK():
#     return json.dumps(spv_client.getNeighbours())

@app.route('/chainbalance')
def returnChainBalance():
    return jsonify(miner.currentChainBalance)

@app.route('/mybalance')
def returnBalance():
    return jsonify(miner.balance)

@app.route('/checkblock')
def checkBlock():
    resp = miner.blockChain.ends[0]
    print(resp.hash)
    return 'testing'

@app.route('/validateblock', methods = ['POST'])
def validateBlock():
    r = request.get_json()
    print(r)
    block = miner.addBlockFromJson(r)
    print(type(block))
    return 'Block added!'
    #print(r)

@app.route('/run')
def run():
    """Do some miner stuff"""
    end_block = miner.mine()
    print('mined a block')
    propogateBlock(end_block)
    print('Block has been sent to neighbours')
    print(neighbours)

    response = 'test'
    #print(response)
    return jsonify(response)


def propogateBlock(block):
    json_block = block.toJson()
    print(json_block)
    for node in neighbours:
        url = 'http://127.0.0.1:'+str(node)+'/validateblock'
        requests.post(url, json=json_block)
        #print(r.json())

def main(argv):
    portnbr = neighbours.pop(int(argv[0]))
    app.run(port=portnbr)

if __name__== "__main__":
    main(sys.argv[1:])
