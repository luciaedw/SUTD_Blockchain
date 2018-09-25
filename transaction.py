import ecdsa
import json
from binascii import hexlify, unhexlify

class Transaction:

    def __init__(self, sender, receiver, amount, signature, comment=""):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature
        self.comment = comment

    # Method for making a new transaction using input fields
    @classmethod
    def new(cls, sender, receiver, amount, signature, comment=""):
        if type(sender) is str:
            sender = sender
        if type(sender) is bytes:
            sender = hexlify(sender).decode()
        elif type(sender) is ecdsa.keys.VerifyingKey:
            sender = hexlify(sender.to_string()).decode()
        return cls(sender, receiver, amount, signature, comment)

    # Print fields for debugging
    def printSelf(self):
        print(self.sender)
        print(self.receiver)
        print(self.amount)
        print(self.signature)
        print(self.comment)

    # Serializes object to JSON string
    def to_json(self):
        return json.dumps(self.__dict__)

    # Instantiates/Deserializes object from JSON string
    @classmethod
    def from_json(cls, inpStr):
        jsonData = json.loads(inpStr)
        jsonKeys = list(jsonData.keys())
        if (
                'sender' not in jsonKeys or 'receiver' not in jsonKeys or 'amount' not in jsonKeys or 'signature' not in jsonKeys):
            raise ValueError('Missing keys in Json object, expecting: sender, receiver, amount, signature')
        else:
            if ('comment' in jsonKeys):
                comment = jsonData['comment']
            else:
                comment = ''
            return cls(jsonData['sender'], jsonData['receiver'], jsonData['amount'], jsonData['signature'], comment)

    # Sign object, takes private key as input
    def sign(self, privKey):
        headerDict = dict(self.__dict__)
        del headerDict['signature']
        headerJson = json.dumps(headerDict, sort_keys=True)
        header = str(headerJson).encode()
        signature = privKey.sign(header)
        self.signature = hexlify(signature).decode()
        return signature

    # Validate signature against expected results
    def validate(self):
        signature = unhexlify(self.signature.encode())
        headerDict = dict(self.__dict__)
        del headerDict['signature']
        headerJson = json.dumps(headerDict, sort_keys=True)
        header = str(headerJson).encode()
        vk = ecdsa.VerifyingKey.from_string(unhexlify(self.sender.encode()))
        return (vk.verify(signature, header))

    # Checks of transactions are the same
    def __eq__(self, trans):
        mySig = unhexlify(self.__dict__['signature'].encode())
        transSig = unhexlify(json.loads(trans.to_json())['signature'].encode())
        return mySig == transSig