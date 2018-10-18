import hashlib
#import transaction
from flask import Flask, request, jsonify
import sys, getopt

class SPV():
    """Light weight client used for sending and receiving transactions.
    Can validate blocks without the entire block(just header),through requesting proof of inclusion.
    Requests proofs of inclusion for it's own transaction."""

    def __init__(self):
        self.pub_keys = None#list of public keys
        self.headers = []#list containing the headers of the longest branch
        self.transactions = [2, 4, 6]#list
        self.pub_key = None
        self.nodes = set()#a set of neighbouring nodes
        self.nonce = 0

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


    def getBlockHeader(self, header):
        #perhanps un load json first?
        self.headers.append(header)

    def checkLongest(self):
        """Make sure we're on the longest branch and if not, swap. Send requests for end state of full nodes."""


    def verifyTrans(self, trans):
        """Requests the proof for a transaction and verifies it"""
        proof=None
        root=None
        #proof = miner.getProof(trans) or
        #trans, proof = miner,getTransProof(pub_key) #we would need the blockheader as well
        added = verifyProof(trans, proof, root)
        None

    def sendTrans(self, receiver, amount, signature, nonce):
        #transaction = Transaction(self.pub_key, receiver, amount, signature, nonce)
        """Create a new transaction and broadcast it to the network"""
        None

    def getNeighbours(self):
        return self.nodes


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

def main(argv):
    #argv contains: [spv.pub_key, port]
    #print('First arg: ' + str(argv[0]))
    #print('Second arg: ' + str(argv[1]))
    spv_client.setPubKey(argv[0])
    #app=Flask(__name__)
    app.run(port=argv[1])

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