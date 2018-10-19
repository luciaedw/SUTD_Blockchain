# Blockchain class for A2Q2, handles forking and adding to any block in a chain

from block import block


class blockChain:
    def __init__(self):
        #self.genesis = block.createBlock(None, '0', None)
        self.genesis = block.createGenesis()
        self.ends = [self.genesis]
        self.blocks = [self.genesis]
        self.allHeaders = [self.genesis.hash]
        self.globalParam = int(
            '0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
            16)

    def add(self, treeRoot, tree, parentBlock=None):
        if parentBlock == None:
            parentBlock = self.ends[0]
        newBlock = block.createBlock(parentBlock, treeRoot, tree)
        while (True):
            if (int(newBlock.getHash(), 16) <= self.globalParam):
                self.blocks.append(newBlock)
                self.allHeaders.append(newBlock.hash)
                break
            else:
                newBlock.reHash()

        print("added block")
        print(newBlock.getHash())
        try:
            self.ends[self.ends.index(parentBlock)] = newBlock
        except ValueError:
            print("chain fork, appending new end")
            self.ends.append(newBlock)
        return newBlock

    # Add a new block to the chain given some parameters, used when another miner discovers a block
    # takes in a tree, previous block header, nonce as POW and time
    def addKnownBlock(self, tree, previousHeader, nonce, time):
        # if previous block exists in chain find that block
        if previousHeader in self.allHeaders:
            for block in self.blocks:
                if block.hash == previousHeader:
                    parentBlock = block

            # Create the new block using the found block as parent and other given params
            newBlock = block.createKnown(tree, parentBlock, nonce, time)
            # Various checks
            if not newBlock.validate():
                print("newblock can't be validated")
            elif newBlock.hash in self.allHeaders:
                print("newBlock already in chain")
            elif int(newBlock.getHash(), 16) > self.globalParam:
                print("newblock hash not within global param")
                print(newBlock.hash)
            else:
                # add new block to list of blocks and header to list of headers, also add new block as an end
                self.blocks.append(newBlock)
                self.allHeaders.append(newBlock.hash)
                try:
                    self.ends[self.ends.index(parentBlock)] = newBlock
                except ValueError:
                    print("chain fork, appending new end")
                    self.ends.append(newBlock)
                return newBlock
        print("unable to add known block")
        return 0

    # Find the longest chain in blockChain
    def resolve(self):
        lengths = []
        for end in self.ends:  # iterate through ends and count length by going backwards
            curLen = 0
            while (end is not self.genesis):
                curLen += 1
                end = end.prev
            lengths.append(curLen)

        maxLen = max(lengths)
        return [maxLen, self.ends[lengths.index(maxLen)]]

    def validate(self):
        for block in self.blocks:

            if not block.validate() or not (int(block.getHash(), 16) <= self.globalParam):
                if (block != self.genesis):
                    return False
        return True