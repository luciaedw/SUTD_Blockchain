# A2Q1 first version of a blockchain, doesn't allow adding to anywhere and only has one end
from block import block


class blockChain:
    def __init__(self):
        self.genesis = block(None, None, '0', None)
        self.end = self.genesis
        self.blocks = [self.genesis]
        self.globalParam = int(
            '00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
            16)

    def add(self, treeRoot, tree):
        newBlock = block(self.end, self.end.getHash(), treeRoot, tree)
        while (True):
            if (int(newBlock.getHash(), 16) <= self.globalParam):
                self.end = newBlock
                self.blocks.append(newBlock)
                break
            else:
                newBlock.reHash()
        print("added block")
        print(newBlock.getHash())

    def validate(self):
        for block in self.blocks:

            if not block.validate() or not (int(block.getHash(), 16) <= self.globalParam):
                if (block != self.genesis):
                    return False
        return True