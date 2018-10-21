from flask import Flask, jsonify, request
import requests, json, hashlib
from spv import SPV
import sys, getopt
from ecdsa import SigningKey
from binascii import hexlify
from transaction import Transaction

app = Flask(__name__)
#testChain = blockChain()
sk = SigningKey.generate() # uses NIST192p
vk = sk.get_verifying_key().to_string()
spv = SPV(sk, hexlify(vk).decode())#, testChain)
spvs = [5003]#, 5004]#, 5002]
miners = [5000, 5001]#, 5002]
neighbours = []
port = None

@app.route('/')
def index():
    return jsonify('Testing')

@app.route('/test2')
def test2():
    return jsonify('Hello World!')

@app.route('/getpubkey')
def getPubKey():
    return jsonify(spv.getPubkey())

@app.route('/gettrans/<idx>')#, methods=['POST', 'GET'])
def getTrans(idx):
    trans = spv.getTransaction(int(idx))
    return jsonify(trans)

@app.route('/getnodespk')
def getNodePK():
    return json.dumps(spv.getNeighbours())

@app.route('/newtrans', methods=['POST'])
def makeTransaction():
    """Make a transaction and send to other miners"""
    r = request.get_json()
    r['receiver'] = spv.neighbours[0]
    trans = spv.createTransaction(r['receiver'], r['amount'], r['message'])
    #print(trans)
    for node in miners:
        url = 'http://127.0.0.1:' + str(node) + '/addtrans'
        requests.post(url, json=trans.to_json())
    return jsonify('Did we get a response?')

@app.route('/addpk', methods=['POST'])
def addPublicKey():
    data = request.get_json()
    print('Public key of neighbour: ' + str(data))
    spv.neighbours.append(data)
    print('Added neighbour')
    return 'Added neighbour'


@app.route('/tellneighbours')
def tellNeighbours():
    for node in (miners + spvs):
        #data = {'pk':spv.pub_key}
        url = 'http://127.0.0.1:'+str(node)+'/addpk'
        requests.post(url, json=spv.pubKey)
    return 'Sent public key'

@app.route('/addheader', methods=['POST'])
def addHeader():
    header = request.get_json()
    print(header)
    return 'Added header'

@app.route('/run')
def run():
    """Do some spv stuff"""
    print('Entering verify')
    spv.verifyTransactions()
    response = 'test'
    print(response)
    return response


def main(argv):
    portnbr = spvs.pop(int(argv[0]))
    port = portnbr
    app.run(port=portnbr)


if __name__== "__main__":
    main(sys.argv[1:])