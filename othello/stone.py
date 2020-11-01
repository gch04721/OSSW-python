from bangtal import *
from state import *

class Stone(Object):
    def __init__(self, BLOCK_STATE, scene, x, y, observer):
        Object.__init__(self, BLOCK_STATE.fileName)
        self.STATE = BLOCK_STATE
        self.initX = 40
        self.initY = 600
        self.x = y
        self.y = x
        self.locate(scene, self.initX + self.x * 80 , self.initY - self.y * 80)
        self.isShow = True
        self.observer = observer
        self.show()

    def onMouseAction(self, x__, y__, action):
        if self.STATE.STATE == POSSIBLE_BLACK().STATE:
            self.observer.possibleBlackClicked(self.x, self.y)
        elif self.STATE.STATE == POSSIBLE_WHITE().STATE:
            self.observer.possibleWhiteClicked(self.x, self.y)
        else:
            print("BLANK")  
    
    def userClicked(self):
        self.observer.possibleWhiteClicked(self.x, self.y)
        
    def changeState(self, STATE):
        if self.STATE.STATE == BLACK().STATE:
            if STATE.STATE == WHITE().STATE:
                self.observer.subBlack()
                self.observer.addWhite()
        elif self.STATE.STATE == WHITE().STATE:
            if STATE.STATE == BLACK().STATE:
                self.observer.addBlack()
                self.observer.subWhite()
        else:
            if STATE.STATE == WHITE().STATE:
                self.observer.addWhite()
            elif STATE.STATE == BLACK().STATE:
                self.observer.addBlack()

        self.STATE = STATE
        self.setImage(STATE.fileName)
        self.show()
        
    def showStone(self):
        self.isShow = True
        self.show()
    
    def hideStone(self):
        self.isShow = False
        self.hide()