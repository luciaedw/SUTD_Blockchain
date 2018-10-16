from blockChain import blockChain
from ecdsa import SigningKey
from binascii import hexlify
from miner import Miner
# Miner tests
miners = []
testChain = blockChain()
for i in range(5):
  sk = SigningKey.generate() # uses NIST192p
  vk = sk.get_verifying_key().to_string()
  newMiner = Miner(sk, hexlify(vk).decode(), testChain)
  miners.append(newMiner)

print(type(sk))

# Mine first block, give it to miner 1 to validate
miners[0].mine()
print(miners[0].balance)
miners[1].validateNewBlock(miners[0].endBlock)
print(miners[1].balance)
print(miners[1].currentChainBalance)
miners[1].updateEndBlock()
print(miners[1].currentChainBalance)
print(miners[1].transactionHistory)

# Create a transaction miner 0 gives miner 1 10 coins, gives transaction to miner 1, who then mines a new block
firstTrans = miners[0].createTransaction(miners[1].pubKey, 10, 'sending miner 1 10')
print('AAAAAAAAAA')
miners[1].addTransaction(firstTrans)
print(miners[1].currentChainBalance)
miners[1].mine()
miners[0].validateNewBlock(miners[1].endBlock)
miners[0].updateEndBlock()

# Create a transaction, miner 1 gives miner 0 10 coins, miner 0 validates and mines a new block, miner 1 does not update end
newTrans = miners[1].createTransaction(miners[0].pubKey, 10,'sending miner 0 10')
miners[0].addTransaction(newTrans)
miners[0].mine()
miners[1].validateNewBlock(miners[0].endBlock)

print(testChain.ends)
print(miners[1].balance)
miners[0].addTransaction(newTrans)
print(miners[0].currentChainBalance)
print(miners[0].balance)

# Create a new transaction, miner 0 gives miner 1 10 coins, miner 1 validates the transaction and mines a new block
# Since the end block was not updated previously, this will create a fork
newTrans = miners[0].createTransaction(miners[1].pubKey, 10,'sending miner 0 10')
miners[1].addTransaction(newTrans)
miners[1].mine()
miners[0].validateNewBlock(miners[1].endBlock)
# Expecting 2 dictionaries, 1 for each branch, one should have miner 0 with 200 coins and miner 1 with 100, the other
# should have miner 0 with 80 coins and miner 1 with 220
print(miners[1].balance)
print(miners[0].balance)