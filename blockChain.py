# Blockchain class for A2Q2, handles forking and adding to any block in a chain

from block import block


class blockChain:
    def __init__(self):
        self.genesis = block(None, '0', None)
        self.ends = [self.genesis]
        self.blocks = [self.genesis]
        self.globalParam = int(
            '0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
            16)

    def add(self, treeRoot, tree, parentBlock=None):
        if parentBlock == None:
            parentBlock = self.ends[0]
        newBlock = block(parentBlock, treeRoot, tree)
        while (True):
            if (int(newBlock.getHash(), 16) <= self.globalParam):
                self.blocks.append(newBlock)
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

    def addKnownBlock(self, newBlock, parentBlock):
        if parentBlock in self.blocks and newBlock.validate() and newBlock not in self.blocks:
            self.blocks.append(newBlock)
            try:
                self.ends[self.ends.index(parentBlock)] = newBlock
            except ValueError:
                print("chain fork, appending new end")
                self.ends.append(newBlock)

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