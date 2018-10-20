import hashlib
import transaction
from flask import Flask, request, jsonify
import sys, getopt
import requests
import json
from transaction import Transaction
from merkleTree import merkleTree

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
        self.miners = [5003]#hard code the miners ports

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