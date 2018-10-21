import requests
import json, hashlib
from transaction import Transaction
from merkleTree import merkleTree

class SPV():
    """Light weight client used for sending and receiving transactions.
    Can validate blocks without the entire block(just header),through requesting proof of inclusion.
    Requests proofs of inclusion for it's own transaction."""

    def __init__(self, privKey, pubKey):
        self.pubKey = pubKey
        self.privateKey = privKey
        self.balance = {}
        self.headers = []#list containing the headers of the longest branch
        self.transactions = [{'receiver':'mary', 'amount':2000}, {'receiver':'anders', 'amount':200}, {'receiver':'mary', 'amount':3000}]#list of all transactions that we have sent
        self.verified_trans = []#a list of all transactions that we have verified
        self.unverified_trans = [{'receiver':'mary', 'amount':2000}, {'receiver':'anders', 'amount':200}, {'receiver':'mary', 'amount':3000}]#list of transactions yet to be verified
        self.neighbours = [] #pk of neighbours
        self.spvs = [5003, 5004]#list of neighbouring nodes
        self.nodes_pk = []
        self.miners = [5000, 5001, 5002]#hard code the miners ports

    def getTransaction(self, idx):
        return self.transactions[idx]
    #
    # def getPubkey(self):
    #     return self.pubKey
    #
    # def setPubKey(self, pub_key):
    #     self.pub_key = pubKey

    def addHeaderFromJson(self, inpStr):
        print('In add header')
        # Parse json, make sure needed fields are there
        jsonData = json.loads(inpStr)
        jsonKeys = list(jsonData.keys())
        if 'prevHead' not in jsonKeys or 'nonce' not in jsonKeys or 'time' not in jsonKeys or 'root' not in jsonKeys:
            raise ValueError(
                'Missing keys in Json object, expecting: root, previousHeader, nonce, and time')
        else:
            print('This is our header: ' + str(jsonData))
            self.headers.append(jsonData)

    def checkLongest(self):
        """Make sure we're on the longest branch and if not, swap. Send requests for end state of full nodes."""
        for miner in self.miners:
            None

    def verifyTransactions(self):
        """Requests the proof for a transaction and verifies it"""
        print('In verify')
        for trans in self.unverified_trans:
            json_trans = trans.to_json()
            for miner in self.miners:
                url = 'http://127.0.0.1:' + str(miner) + '/gettransproof'
                #print(trans)
                #print(url)
                r = requests.get(url, json=json_trans) #r will contain the block header/(or just the hash of the header) and proof for the transaction
                #print(r.json()['found'])
                if r.json()['found'] == True:
                    verified = self.verifyProof(trans, r['proof'], r['root'])
                    if verified:
                        self.unverified_trans.remove(trans)
                        self.verified_trans.append(trans)
        print(self.verified_trans)
        print(self.unverified_trans)


    def createTransaction(self, receiver, amount, message):
        newTransaction = Transaction.new(self.pubKey, receiver, amount, 'placeholder', message)
        newTransaction.sign(self.privKey)
        self.unverified_trans.append(newTransaction)
        return newTransaction


    def verifyProof(self, transaction, proof, root):
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