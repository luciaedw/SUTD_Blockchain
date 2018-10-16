from merkleTree import merkleTree
from transaction import Transaction

class Miner:
    def __init__(self, privKey, pubKey, blockChain):
        self.balance = [{}]  # List of dictionaries, represents balance of each address in a given fork
        self.currentChainBalance = {}  # current balance dictionary on working fork
        self.privKey = privKey
        self.pubKey = pubKey
        self.blockChain = blockChain
        self.allTransactions = []  # List of current transactions, used in mine to generate merkle tree
        self.transactionHistory = []  # History of all transaction signatures, prevent double spend
        self.endBlock = blockChain.resolve()[1]

    # Function for adding 100 coins to the miner as their first transaction
    def addReward(self):
        myTransaction = Transaction.new('0', self.pubKey, 100, 'a', 'generate coins')
        myTransaction.sign(self.privKey)
        if (self.pubKey in self.currentChainBalance.keys()):
            self.currentChainBalance[self.pubKey] += 100
        else:
            self.currentChainBalance[self.pubKey] = 100
        self.allTransactions.append(myTransaction)

    # Mining function
    def mine(self):
        if len(self.allTransactions) == 0:  # Make sure reward is there
            self.addReward()
        # Create merkle tree using all the transaction currently in miner
        newTree = merkleTree()
        for transaction in self.allTransactions:
            newTree.add(transaction)

        newTree.build()

        # Mine for new block
        self.endBlock = self.blockChain.add(newTree.getRootHash(), newTree, self.endBlock)
        endBlockIndex = self.blockChain.ends.index(self.endBlock)
        # Consolidate working balance into balance dictionaries, if no dictionary is present for
        # A given branch, append a new one to the list
        if len(self.balance) > endBlockIndex:
            self.balance[endBlockIndex] = dict(self.currentChainBalance)
        else:
            print("ADDING NEW BALANCE DICT")
            self.balance.append(dict(self.currentChainBalance))
        self.allTransactions=[]
        return self.endBlock

    # Add a transaction from someone else into local transaction list
    def addTransaction(self, transaction):
        # Make sure reward is there
        if len(self.allTransactions) == 0:
            self.addReward()

        # Check if transaction is valid using: validate function, signature not used previously, sender has enough money in the current chain
        # If checks are ok, append to local list and modify working balance dict
        if type(transaction) is not Transaction:
            print("transaction is not a Transaction class")
        elif not transaction.validate():
            print("transaction is not valid")
        elif transaction.signature in self.transactionHistory:
            print("transaction already used")
        elif transaction.sender not in self.currentChainBalance.keys():
            print("transaction sender not in fork")
        elif self.currentChainBalance[transaction.sender] <= transaction.amount:
            print("sender does not have enough coins")
        else:
            print(self.currentChainBalance)
            print(self.currentChainBalance[transaction.sender])
            self.allTransactions.append(transaction)
            self.transactionHistory.append(transaction.signature)
            self.currentChainBalance[transaction.sender] -= transaction.amount
            self.currentChainBalance[transaction.receiver] += transaction.amount

    # Create a new transaction for another miner
    def createTransaction(self, receiver, amount, message):
        newTransaction = Transaction.new(self.pubKey, receiver, amount, 'placeholder', message)
        newTransaction.sign(self.privKey)
        return newTransaction

    # helper function to update a balance dictionary given a new block
    def updateBalanceDict(self, someBlock, endPos):
        # Extract all transactions in the block, and pick the correct balance table using index of end block
        newTransactions = someBlock.tree.entries
        balanceTable = self.balance[endPos]
        # Iterate through transactions and modify balance table accordingly
        for transaction in newTransactions:
            sender = transaction.sender
            receiver = transaction.receiver
            amount = transaction.amount
            if sender not in balanceTable.keys():
                balanceTable[sender] = 0
            if receiver not in balanceTable.keys():
                balanceTable[receiver] = 0
            balanceTable[sender] -= amount
            balanceTable[receiver] += amount
            self.transactionHistory.append(transaction.signature)

    # Update balance tables given a new block
    def updateBalances(self, newBlock):
        endPosition = self.blockChain.ends.index(newBlock)
        print("END POSITION IS")
        print(endPosition)
        # Determine if the new block is a fork, if not call updateBalanceDict using the block
        if (len(self.balance) > endPosition):
            self.updateBalanceDict(newBlock, endPosition)
        # If the new block is a fork then we must make a new balance table for the fork, follow the chain from the
        # New block to the genesis block calling updateBalanceDict on each block
        else:
            print('ADDING NEW BALANCE DICT')
            self.balance.append({})
            while (True):
                if (newBlock == self.blockChain.genesis):
                    break
                else:
                    self.updateBalanceDict(newBlock, endPosition)
                    newBlock = newBlock.prev

    # Update local endBlock to be the endblock in the longest chain
    def updateEndBlock(self):
        longestEnd = self.blockChain.resolve()[1]
        self.endBlock = longestEnd
        endBlockIndex = self.blockChain.ends.index(longestEnd)
        self.currentChainBalance = dict(self.balance[endBlockIndex])
        self.allTransactions = []

    # Validate a block mined by someone else and if valid, update local balance tables
    def validateNewBlock(self, newBlock):
        if newBlock.validate():
            self.updateBalances(newBlock)