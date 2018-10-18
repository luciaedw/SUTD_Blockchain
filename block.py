# Block class

import json
import hashlib
import time


class block:
    def __init__(self, prev, prevHead, root, tree, curTime, nonce):
        self.prev = prev
        self.prevHead = prevHead
        self.root = root
        self.tree = tree
        self.time = curTime
        self.nonce = nonce
        self.hash = 0
        self.hash = self.hashSelf()

    # Normal method for creating a new block, given a previous block, root and tree
    @classmethod
    def createBlock(cls, prev, root, tree):
        if not prev:
            prevHead = None
        else:
            prevHead = prev.getHash()
        curTime = int(time.time())
        nonce = 0
        return cls(prev, prevHead, root, tree, curTime, nonce)

    # Method for creating a block object if POW is already known
    @classmethod
    def createKnown(cls, tree, parentBlock, nonce, time):
        print(tree.getRootHash())
        print(tree.entries[0].to_json())
        return cls(parentBlock, parentBlock.getHash(), tree.getRootHash(), tree, time, nonce)

    @classmethod
    def createGenesis(cls):
        return cls(None, None, '0', None, 0, 0)

    def hashSelf(self):
        headerDict = dict(self.__dict__)
        del headerDict['prev']
        del headerDict['tree']
        del headerDict['hash']
        jsonTrans = json.dumps(headerDict)
        hashVal = hashlib.sha512(jsonTrans.encode()).hexdigest()
        self.hash = hashVal
        return hashVal

    def getHash(self):
        return self.hash

    def reHash(self):
        self.nonce += 1
        self.hash = self.hashSelf()
        return self.hash

    def validate(self):
        headerDict = dict(self.__dict__)
        del headerDict['prev']
        del headerDict['tree']
        del headerDict['hash']
        jsonTrans = json.dumps(headerDict)
        if self.tree:
            return (self.getHash() == hashlib.sha512(
                jsonTrans.encode()).hexdigest() and self.tree.validate()) and self.prev.getHash() == self.prevHead
        else:
            return (self.getHash() == hashlib.sha512(jsonTrans.encode()).hexdigest())

    # Serializes block into a json string
    def toJson(self):
        jsonDict = {}
        transactions = self.tree.entries
        jsonDict['transactions'] = []
        jsonDict['previousHeader'] = self.prevHead
        jsonDict['nonce'] = self.nonce
        jsonDict['time'] = self.time
        for transaction in transactions:
            jsonDict['transactions'].append(transaction.to_json())

        return json.dumps(jsonDict)
