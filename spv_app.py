from flask import Flask, jsonify, request
import requests, json, hashlib
import spv
import sys, getopt
from ecdsa import SigningKey
from binascii import hexlify
from transaction import Transaction

app = Flask(__name__)
#testChain = blockChain()
sk = SigningKey.generate() # uses NIST192p
vk = sk.get_verifying_key().to_string()
miner = Miner(sk, hexlify(vk).decode(), testChain)
neighbours = [5000, 5001]#, 5002]
port = None

@app.route('/')
def index():
    return jsonify('Testing')

@app.route('/test2')
def test2():
    return jsonify('Hello World!')

@app.route('/getpubkey')
def getPubKey():
    return jsonify(spv_client.getPubkey())

@app.route('/updateNonce', methods=['GET'])
def updateNonce():
    spv_client.updateNonce()
    return jsonify(spv_client.getNonce())

@app.route('/gettrans/<idx>')#, methods=['POST', 'GET'])
def getTrans(idx):
    trans = spv_client.getTransaction(int(idx))
    return jsonify(trans)

@app.route('/getnodespk')
def getNodePK():
    return json.dumps(spv_client.getNeighbours())


@app.route('/run')
def run():
    """Do some spv stuff"""
    print('Entering verify')
    spv_client.verifyTransactions()
    #for trans in spv_client.transactions:
    #for node in spv_client.nodes:
    #    url = 'http://127.0.0.1:' + str(node) + '/getpubkey'
    #    node_pk = requests.get(url).json()
    #    #print(str(node_pk), type(node_pk))
    #    if str(node_pk) not in spv_client.nodes_pk:
    #        spv_client.nodes_pk.append(str(node_pk))
    #        response = 'Added a neighbours pk'
    #    else:
    #        response = 'We already knew that neighbours pk'
    response = 'test'
    print(response)
    return response


def main(argv):
    portnbr = neighbours.pop(int(argv[0]))
    port = portnbr
    app.run(port=portnbr)


if __name__== "__main__":
    main(sys.argv[1:])