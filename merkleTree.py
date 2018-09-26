# Class for nodes in merkle tree, keeps track of parents, children, and height

import hashlib

class MerkleNode:
    def __init__(self, leftChild, rightChild, hashVal):
        self.parent = None
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.hashVal = hashVal
        if (leftChild == None):
            self.height = 0
        else:
            self.height = leftChild.getHeight() + 1

    def getHeight(self):
        return self.height

    def getHash(self):
        return self.hashVal

    def setParent(self, parentNode):
        self.parent = parentNode

    def getParent(self):
        return self.parent


# Merkle tree implementation, keeps track of nodes(in a dictionary), height, entries(items to be added)
# rootNode, and the root hash
class MerkleTree:
    def __init__(self):
        self.nodes = dict()
        self.height = 0
        self.entries = []
        self.rootNode = None
        self.rootHash = ''

    def getRoot(self):
        return self.rootNode

    def getRootHash(self):
        return self.rootHash

    # Additem to entries, a list of all items used to build tree later
    def add(self, transaction):
        self.entries.append(transaction)

    # Builds a merkle tree using items from entries
    def build(self):
        self.nodes = dict()
        stack = list(self.entries)
        self.height = 0
        if (len(stack) == 0):
            return 0

        else:
            for i in range(len(stack)):
                item = stack.pop(0)
                itemHash = hashlib.sha512(('0' + item.to_json()).encode()).hexdigest()

                itemNode = MerkleNode(None, None, itemHash)
                self.nodes[itemHash] = itemNode
                stack.append(itemNode)

        while (len(stack) > 1):
            leftNode = stack.pop(0)
            rightNode = stack.pop(0)
            newHash = hashlib.sha512(('1' + leftNode.getHash() + rightNode.getHash()).encode()).hexdigest()
            newNode = MerkleNode(leftNode, rightNode, newHash)
            stack.append(newNode)
            self.nodes[newHash] = newNode
            leftNode.setParent(newNode)
            rightNode.setParent(newNode)
        self.rootNode = stack[0]
        self.rootHash = stack[0].getHash()
        return self.rootHash

    # Gets a proof as a 2d list, the first element of each index represents which
    # side the hash is from
    def getProof(self, transaction):
        proof = []
        transHash = hashlib.sha512(('0' + transaction.to_json()).encode()).hexdigest()
        if transHash in self.nodes.keys():
            transNode = self.nodes[transHash]
        else:
            return proof
        while (transNode is not self.rootNode):
            if (transNode.getParent().leftChild is transNode):
                proof.append(['right', transNode.getParent().rightChild.getHash()])
            else:
                proof.append(['left', transNode.getParent().leftChild.getHash()])
            transNode = transNode.getParent()
        return (proof)

    # Verify proof against root
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

    def validate(self):
        for transaction in self.entries:
            proof = self.getProof(transaction)
            if not self.verifyProof(transaction, proof, self.rootHash) or not transaction.validate():
                return False
        return True