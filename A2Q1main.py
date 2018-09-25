# basic tests for blockChainV1, makes a blockchain and validates it

from binascii import hexlify
import random
from ecdsa import SigningKey
from transaction import Transaction
from merkleTree import merkleTree
from blockChainV2 import blockChain

# Testing Blockchain Stuff

testChain = blockChain()

for i in range(5):
  print("building tree")
  trannies = []
  for i in range(random.randint(10,100)):
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.get_verifying_key().to_string()
    newTrans = Transaction.new(hexlify(vk).decode(),'b',random.randint(100,1000),'a',i)
    newTrans.sign(sk)
    trannies.append(newTrans)
    if i%100 == 0:
      print('built %d entries'%(i))

  testTree = merkleTree()

  for t in trannies:
    testTree.add(t)

  testTree.build()
  print('done building')
  print('adding block')
  
  newRootHash = testTree.getRootHash()
  testChain.add(newRootHash, testTree)
  
# Expecting True, 0, True
print(testChain.genesis.validate())
print(testChain.genesis.root)
print(testChain.validate())