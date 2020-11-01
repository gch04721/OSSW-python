from state import *
from stone import *
from observer import Observer

class MainModel:
    def __init__(self, mainView, w, h):
        self.mainView = mainView
        self.w = w
        self.h = h
        self.board_width = 640
        self.board_heigth = 640

        self.blackTurn = True

        self.observer = Observer(self)
        self.recalc = False
        self.end = False

        self.blackStoneNum = 0
        self.whiteStoneNum = 0

        self.possibleWhiteNum = {}

        self.computer = None

        self.initStone()

    def initStone(self):
        self.stoneArr = []
        self.candidateStoneArr = []
        for i in range(self.w):
            tempArr = []
            for j in range(self.h):
                tempArr.append(Stone(BLANK(), self.mainView.mainScene, j, i, self.observer))

            self.stoneArr.append(tempArr)

        self.stoneArr[int((self.h / 2 ))- 1][int((self.w / 2 ))- 1].changeState(WHITE())
        self.stoneArr[int((self.h / 2 ))][int((self.w / 2 ))].changeState(WHITE())
        self.stoneArr[int((self.h / 2 ))- 1][int((self.w / 2 ))].changeState(BLACK())
        self.stoneArr[int((self.h / 2 ))][int((self.w / 2 ))- 1].changeState(BLACK())
        self.updatePossible()
        
    def clearPossible(self):
        for i in range(self.h):
            for j in range(self.w):
                if self.stoneArr[i][j].STATE.STATE == POSSIBLE_WHITE().STATE:
                    self.stoneArr[i][j].changeState(BLANK())
                elif self.stoneArr[i][j].STATE.STATE == POSSIBLE_BLACK().STATE:
                    self.stoneArr[i][j].changeState(BLANK())
        self.possibleBlack = False
        self.possibleWhite = False
        self.possibleWhiteNum.clear()
        
    def updatePossible(self):
        self.clearPossible()
        for i in range(self.w):
            for j in range(self.h):
                if self.stoneArr[i][j].STATE.STATE == BLANK().STATE:
                    if self.checkIsPossibleBlack(i, j):
                        if self.blackTurn:
                            self.stoneArr[i][j].changeState(POSSIBLE_BLACK())
                        self.possibleBlack = True

                    if self.checkIsPossibleWhite(i, j):
                        if not self.blackTurn:
                            self.stoneArr[i][j].changeState(POSSIBLE_WHITE())
                        self.possibleWhite = True
                        
        if not self.possibleBlack:
            if not self.possibleWhite:
               self.mainView.gameEnd(self.blackStoneNum > self.whiteStoneNum)
               return
            else:
                if self.blackTurn:
                    self.blackTurn = not self.blackTurn
                    self.updatePossible()
        else:
            if not self.possibleWhite:
                if not self.blackTurn:
                    self.blackTurn = not self.blackTurn
                    self.updatePossible()

        if self.computer != None:
            if not self.blackTurn:
                self.computer.myTurn()
                

    def checkIsPossibleBlack(self, i, j):
        directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0,1], [1, -1], [1, 0], [1,1]]
        
        for i_ in range(self.h):
            dx = directions[i_][0]
            dy = directions[i_][1]

            x = i + dx
            y = j + dy
            ct = 0

            while x >= 0 and y >=0 and x < self.w and y < self.h and self.stoneArr[x][y].STATE.STATE == WHITE().STATE:
                ct += 1
                x += dx
                y += dy
            
            if x >= 0 and y >=0 and x < self.w and y < self.h and self.stoneArr[x][y].STATE.STATE == BLACK().STATE and ct >0:
                return True

        return False

    def checkIsPossibleWhite(self, i, j):
        directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0,1], [1, -1], [1, 0], [1,1]]
        self.possibleWhiteNum[(i, j)] = 0
        
        for i_ in range(self.h):
            dx = directions[i_][0]
            dy = directions[i_][1]

            x = i + dx
            y = j + dy
            ct = 0
            while x >= 0 and y >=0 and x < self.w and y < self.h and self.stoneArr[x][y].STATE.STATE == BLACK().STATE:
                ct += 1
                x += dx
                y += dy
            
            if x >= 0 and y >=0 and x < self.w and y < self.h and self.stoneArr[x][y].STATE.STATE == WHITE().STATE and ct >0:
                self.possibleWhiteNum[(i, j)] += ct
                
        if self.possibleWhiteNum[(i,j)] > 0:
            return True

        del self.possibleWhiteNum[(i, j)]    
        return False
        
    def flipWhiteStones(self, x, y):
        if self.blackTurn:
            self.stoneArr[x][y].changeState(BLACK())

        directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0,1], [1, -1], [1, 0], [1,1]]
        for i in range(8):
            dx = directions[i][0]
            dy  = directions[i][1]

            x_ = x + dx
            y_ = y + dy
            flipList_x = []
            flipList_y = []
            flipCt = 0
            while x_ >= 0 and y_ >=0 and x_ < self.w and y_ < self.h and\
                 ((self.stoneArr[x_][y_].STATE.STATE == WHITE().STATE and self.blackTurn)):    
                flipList_x.append(x_)
                flipList_y.append(y_)
                flipCt += 1
                x_ += dx
                y_ += dy

            if x_ >= 0 and y_ >=0 and x_ < self.w and y_ < self.h and\
                 ((self.stoneArr[x_][y_].STATE.STATE == BLACK().STATE and self.blackTurn)):
                 for j in range(flipCt):    
                    self.stoneArr[flipList_x[j]][flipList_y[j]].changeState(BLACK())

        self.mainView.updateStoneNum()
        self.blackTurn = not self.blackTurn
    
    def flipBlackStones(self, x, y):
        if not self.blackTurn:
            self.stoneArr[x][y].changeState(WHITE())

        directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0,1], [1, -1], [1, 0], [1,1]]
        for i in range(8):
            dx = directions[i][0]
            dy  = directions[i][1]

            x_ = x + dx
            y_ = y + dy

            flipList_x = []
            flipList_y = []
            flipCt = 0

            while x_ >= 0 and y_ >=0 and x_ < self.w and y_ < self.h and\
                 ((self.stoneArr[x_][y_].STATE.STATE == BLACK().STATE and not self.blackTurn)):    
                flipList_x.append(x_)
                flipList_y.append(y_)
                flipCt += 1
                x_ += dx
                y_ += dy

            if x_ >= 0 and y_ >=0 and x_ < self.w and y_ < self.h and\
                 ((self.stoneArr[x_][y_].STATE.STATE == WHITE().STATE and not self.blackTurn)):
                 for j in range(flipCt):    
                    self.stoneArr[flipList_x[j]][flipList_y[j]].changeState(WHITE())   

        self.mainView.updateStoneNum()        
        self.blackTurn = not self.blackTurn