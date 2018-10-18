import hashlib
import transaction
from flask import Flask, request, jsonify
import sys, getopt
import requests
import json

class SPV():
    """Light weight client used for sending and receiving transactions.
    Can validate blocks without the entire block(just header),through requesting proof of inclusion.
    Requests proofs of inclusion for it's own transaction."""

    def __init__(self):
        self.pub_key = None
        self.headers = []#list containing the headers of the longest branch
        self.transactions = [{'receiver':'mary', 'amount':2000}, {'receiver':'anders', 'amount':200}, {'receiver':'mary', 'amount':3000}]#list of all transactions that we have sent
        self.verified_trans = []#a list of all transactions that we have verified
        self.unverified_trans = [{'receiver':'mary', 'amount':2000}, {'receiver':'anders', 'amount':200}, {'receiver':'mary', 'amount':3000}]#list of transactions yet to be verified
        self.pub_keys_neighbours = []
        self.nodes = [5000, 5001, 5002]#list of neighbouring nodes
        self.nodes_pk = []
        self.nonce = 0
        self.miners = [5003]#hard code the miners ports

    def updateNonce(self):
        self.nonce += 1
        return self.nonce

    def getTransaction(self, idx):
        return self.transactions[idx]

    def getPubkey(self):
        return self.pub_key

    def setPubKey(self, pub_key):
        self.pub_key = pub_key

    def getNonce(self):
        return self.nonce

    def addNeighbour(self, address):
        """Might just make a static list of neighbours"""
        #print('Address: %' %address)
        if address != None:
            self.nodes.add(address)


    def addBlockHeader(self, header):
        #perhanps unload json first?
        self.headers.append(header)

    def checkLongest(self):
        """Make sure we're on the longest branch and if not, swap. Send requests for end state of full nodes."""
        for miner in self.miners:
            None



    def verifyTransactions(self):
        """Requests the proof for a transaction and verifies it"""
        print('In verufy')
        for trans in self.unverified_trans:
            for miner in self.miners:
                url = 'http://127.0.0.1:' + str(miner) + '/gettransproof'
                #print(trans)
                #print(url)
                r = requests.get(url, json=trans) #r will contain the block header/(or just the hash of the header) and proof for the transaction
                #print(r.json()['found'])
                if r.json()['found'] == True:
                    #for now move to verified when we found it, we will have to verify the proof too
                    self.unverified_trans.remove(trans)
                    self.verified_trans.append(trans)
        print(self.verified_trans)
        print(self.unverified_trans)
                #if r.json()['found'] == True:
                #    header = r.json()['header'] #or hash, depending on implementation
                    #if(verifyProof(trans, r.json()['proof'], header['root'])):
                    #    self.verified_trans.append(trans)
                    #    break

    def sendTrans(self, receiver, amount, signature, nonce):
        #transaction = Transaction(self.pub_key, receiver, amount, signature, nonce)
        """Create a new transaction and broadcast it to the network"""
        None

    def getNeighbours(self):
        """Return public keys of known nodes"""
        return self.nodes_pk



app = Flask(__name__)
spv_client = SPV()

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
    #argv contains: [spv.pub_key, port[idx]]
    #print('First arg: ' + str(argv[0]))
    #print('Second arg: ' + str(argv[1]))
    spv_client.setPubKey(argv[0])
    #app=Flask(__name__)
    portnbr = spv_client.nodes.pop(int(argv[1]))
    app.run(port=portnbr)

if __name__== "__main__":
    main(sys.argv[1:])



# @app.route('/nodes/register', methods=['POST'])
# def registerNodes():
#     values = request.get_json()
#     print(values)
#     #nodes = values.get('nodes')
#     node_adr = values['nodes']
#     if node_adr is None:
#         return "Error: Please supply a valid list of nodes", 400
#
#     #for node in nodes:
#     #    print('Node: ' + str(node))
#     spv_client.addNeighbour(node_adr)
#         #parsed_url = urlparse(node)
#         #print('Parsed address: ' + str(parsed_url))
#         #nodes_list.add(parsed_url.netloc)
#     #print(len(nodes_list))
#     #print(nodes_list)
#     response = {
#         'message': 'New nodes have been added',
#         'total_nodes': list(spv_client.nodes),
#     }
#     return jsonify(response), 201



# Verify proof against root
def verifyProof(transaction, proof, root):
    transHash = hashlib.sha512(('0' + transaction.to_json()).encode()).hexdigest()
    nextHash = transHash
    while (len(proof) > 0):
        partnerHash = proof.pop(0)
        if partnerHash[0] == 'left':
            nextHash = hashlib.sha512(("1" + partnerHash[1] + nextHash).encode()).hexdigest()
        else:
            nextHash = hashlib.sha512(("1" + nextHash + partnerHash[1]).encode()).hexdigest()

    if (nextHash == root):
        return True
    else:
        return False