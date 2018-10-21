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
from transaction import Transaction

app = Flask(__name__)

testChain = blockChain()
sk = SigningKey.generate() # uses NIST192p
vk = sk.get_verifying_key().to_string()
miner = Miner(sk, hexlify(vk).decode(), testChain)
neighbours = [5000, 5001]#, 5002]#, 5002]
spvs=[5003]#, 5004]
port = None

@app.route('/')
def index():
    return jsonify('Testing')

@app.route('/test2')
def test2():
    return jsonify('Hello World!')

@app.route('/getpubkey')
def getPubKey():
    return jsonify(miner.pubKey)

@app.route('/addpk', methods=['POST'])
def addPublicKey():
    data = request.get_json()
    print('Public key of neighbour: ' + str(data))
    miner.neighbours.append(data)
    print('Added neighbour')
    return 'Added neighbour'


@app.route('/tellneighbours')
def tellNeighbours():
    for node in (neighbours + spvs):
        data = {'pk':miner.pubKey}
        url = 'http://127.0.0.1:'+str(node)+'/addpk'
        requests.post(url, json=miner.pubKey)
    return 'Sent public key'

@app.route('/transactionlist')
def returnTransactionList():
    return jsonify(miner.allTransactions)


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
    miner.updateEndBlock()
    print(type(block))
    return 'Block added!'
    #print(r)

@app.route('/mine')
def mineAndSend():
    """Do some miner stuff"""
    end_block = miner.mine()
    print('mined a block')
    propogateBlock(end_block)
    print('Block has been sent to neighbours: ' + str(neighbours))
    response = 'test'
    #print(response)
    return jsonify(response)


@app.route('/addtrans', methods=['POST'])
def addTransaction():
    trans = request.get_json()
    trans = Transaction.from_json(trans)
    miner.addTransaction(trans)
    return jsonify('test')

@app.route('/newtrans', methods=['POST'])
def makeTransaction():
    """Make a transaction and send to other miners"""
    r = request.get_json()
    r['receiver'] = miner.neighbours[0]
    trans = miner.createTransaction(r['receiver'], r['amount'], r['message'])
    #print(trans)
    for node in neighbours:
        url = 'http://127.0.0.1:' + str(node) + '/addtrans'
        requests.post(url, json=trans.to_json())
    return jsonify('Did we get a response?')

def propogateBlock(block):
    json_block = block.toJson()
    header = {'prevHead':block.prev.getHash(), 'root':block.root, 'time':block.time, 'nonce':block.nonce}
    #print(json_block)
    for node in neighbours:
        url = 'http://127.0.0.1:'+str(node)+'/validateblock'
        requests.post(url, json=json_block)
        #print(r.json())
    for node in spvs:
        url = 'http://127.0.0.1:' + str(node) + '/addheader'
        requests.post(url, json=header)
        # print(r.json())

def main(argv):
    portnbr = neighbours.pop(int(argv[0]))
    port = portnbr
    app.run(port=portnbr)


if __name__== "__main__":
    main(sys.argv[1:])
