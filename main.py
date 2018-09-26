# Basic tests for A2Q2, makes a blockchain and verifies it, also adds a fork

from binascii import hexlify
import random
from ecdsa import SigningKey
from transaction import Transaction
from merkleTree import merkleTree
from blockChain import blockChain

# Testing Blockchain Stuff

testChain = blockChain()
testBlocks = []
for i in range(5):
  print("building tree")
  trannies = []
  for i in range(random.randint(10,100)):
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.get_verifying_key().to_string()
    newTrans = Transaction.new(hexlify(vk).decode(),'b',random.randint(100,1000),'a',i)
    newTrans.sign(sk)
    trannies.append(newTrans)

  testTree = merkleTree()

  for t in trannies:
    testTree.add(t)

  testTree.build()
  print('done building')
  print('adding block')
  
  newRootHash = testTree.getRootHash()
  testBlocks.append(testChain.add(newRootHash, testTree))
  
# Expecting True, True
print(testChain.genesis.validate())
print(testChain.validate())

# Testing Blockchain Stuff
from ecdsa import SigningKey
pBlock = testBlocks[2]
for i in range(5):
  print("building tree")
  trannies = []
  for i in range(random.randint(10,100)):
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.get_verifying_key().to_string()
    newTrans = Transaction.new(hexlify(vk).decode(),'b',random.randint(100,1000),'a',i)
    newTrans.sign(sk)
    trannies.append(newTrans)

  testTree = merkleTree()

  for t in trannies:
    testTree.add(t)

  testTree.build()
  print('done building')
  print('adding block')
  
  newRootHash = testTree.getRootHash()
  pBlock = testChain.add(newRootHash, testTree, pBlock)
  testBlocks.append(pBlock)  
  
print(testChain.genesis.validate())
print(testChain.genesis.root)

# Expecting chain length 8, and most recently added block as chain end
a = testChain.resolve()
print(a)
print(testBlocks)
print(testChain.ends)