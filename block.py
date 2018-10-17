# Block class

import json
import hashlib
import time


class block:
    def __init__(self, prev, root, tree):
        self.prev = prev
        if not prev:
            self.prevHead = None
        else:
            self.prevHead = self.prev.getHash()

        self.root = root
        self.tree = tree
        self.time = int(time.time())
        self.nonce = 0
        self.hash = 0
        self.hash = self.hashSelf()

    def hashSelf(self):
        headerDict = dict(self.__dict__)
        del headerDict['prev']
        del headerDict['tree']
        del headerDict['hash']
        jsonTrans = json.dumps(headerDict)

        return hashlib.sha512(jsonTrans.encode()).hexdigest()

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