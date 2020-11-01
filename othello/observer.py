class Observer:
    def __init__(self, model, computer = False):
        self.model = model
    
    def possibleBlackClicked(self, x, y):
        self.model.flipWhiteStones(x, y)
        self.model.updatePossible()

    def possibleWhiteClicked(self, x, y):
        self.model.flipBlackStones(x, y)
        self.model.updatePossible()

    def addBlack(self):
        self.model.blackStoneNum += 1
    
    def addWhite(self):
        self.model.whiteStoneNum += 1

    def subBlack(self):
        self.model.blackStoneNum -= 1
        if self.model.blackStoneNum < 0:
            self.model.blackStoneNum = 0
    
    def subWhite(self):
        self.model.whiteStoneNum -=1 
        if self.model.whiteStoneNum < 0:
            self.model.whiteStoneNum = 0