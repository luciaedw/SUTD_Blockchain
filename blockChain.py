# Blockchain class for A2Q2, handles forking and adding to any block in a chain

from block import block

class blockChain:
    def __init__(self):
        self.genesis = block(None, None, '0', None)
        self.ends = [self.genesis]
        self.blocks = [self.genesis]
        self.globalParam = int(
            '00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
            16)

    def add(self, treeRoot, tree, parentBlock=None):
        if parentBlock == None:
            parentBlock = self.ends[0]
        newBlock = block(parentBlock, parentBlock.getHash(), treeRoot, tree)
        while (True):
            if (int(newBlock.getHash(), 16) <= self.globalParam):
                self.end = newBlock
                self.blocks.append(newBlock)
                break
            else:
                newBlock.reHash()

        print("added block")
        print(newBlock.getHash())
        self.ends.append(newBlock)
        try:
            self.ends.remove(parentBlock)
        except ValueError:
            print("chain fork")
        return newBlock

    def resolve(self):
        lengths = []
        for end in self.ends:
            curLen = 0
            while (True):
                if end.prev == self.genesis:
                    lengths.append(curLen + 1)
                    break
                else:
                    curLen += 1
                    end = end.prev

        maxLen = max(lengths)
        return [maxLen, self.ends[lengths.index(maxLen)]]

    def validate(self):
        for block in self.blocks:

            if not block.validate() or not (int(block.getHash(), 16) <= self.globalParam):
                if (block != self.genesis):
                    return False
        return True

