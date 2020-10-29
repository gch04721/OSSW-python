from bangtal import *

turn =True

class BLANK:
    def __init__(self):
        self.STATE = "BLANK"
        self.fileName = "images/blank.png"

class POSSIBLE_BLACK:
    def __init__(self):
        self.STATE = "POSSIBLE_BLACK"
        self.fileName = 'images/black possible.png'

class POSSIBLE_WHITE:
    def __init__(self):
        self.STATE = "POSSIBLE_WHITE"
        self.fileName = "images/white possible.png"

class BLACK:
    def __init__(self):
        self.STATE = "BLACK"
        self.fileName = "images/black.png"

class WHITE:
    def __init__(self):
        self.STATE = "WHITE"
        self.fileName = "images/white.png"

class Stone(Object):
    def __init__(self, BLOCK_STATE, scene, x, y):
        
        Object.__init__(self, BLOCK_STATE.fileName)
        global turn
        self.STATE = BLOCK_STATE
        self.locate(scene, x, y)
        self.isShow = True
        self.show()

    def onMouseAction(self, x, y, action):
        if self.STATE.STATE == POSSIBLE_BLACK().STATE:
            self.changeState(BLACK())
            turn = not turn
        elif self.STATE.STATE == POSSIBLE_WHITE().STATE:
            self.changeState(WHITE())
            turn = not turn
        else:
            print("BLANK")  

    def changeState(self, STATE):
        self.STATE = STATE
        self.setImage(STATE.fileName)
        self.show()
        
    def showStone(self):
        self.isShow = True
        self.show()
    
    def hideStone(self):
        self.isShow = False
        self.hide()


class MainClass:
    def __init__(self):
        global turn
        self.mainScene = Scene('main', 'images/background.png')
        self.board = Object('images/board.png')
        self.board.locate(self.mainScene, 40, 40)
        self.board.show()
        self.initX = 40
        self.initY = 600

        self.board_width = 640
        self.board_heigth = 640

        self.initStone()

    def initStone(self):
        self.stoneArr = []
        self.candidateStoneArr = []
        for i in range(8):
            tempArr = []
            for j in range(8):
                tempArr.append(Stone(BLANK(), self.mainScene, self.initX + j * 80, self.initY - i * 80))

            self.stoneArr.append(tempArr)

        self.numBlack = 2
        self.numWhite = 2
        self.stoneArr[3][3].changeState(WHITE())
        self.stoneArr[4][4].changeState(WHITE())
        self.stoneArr[3][4].changeState(BLACK())
        self.stoneArr[4][3].changeState(BLACK())

        self.updatePossible()
        

    def updatePossible(self):
        for i in range(8):
            for j in range(8):
                if self.stoneArr[i][j].STATE.STATE == BLANK().STATE:
                    if self.checkIsPossibleWhite(i,j):
                        self.stoneArr[i][j].changeState(POSSIBLE_WHITE())

                    if self.checkIsPossibleBlack(i,j):
                        self.stoneArr[i][j].changeState(POSSIBLE_BLACK())
        for i in range(8):
            for j in range(8):
                if turn:
                    if self.stoneArr[i][j].STATE.STATE == POSSIBLE_BLACK().STATE:
                        self.stoneArr[i][j].showStone()
                    if self.stoneArr[i][j].STATE.STATE == POSSIBLE_WHITE().STATE:
                        self.stoneArr[i][j].hideStone()
                else:
                    if self.stoneArr[i][j].STATE.STATE == POSSIBLE_BLACK().STATE:
                        self.stoneArr[i][j].hideStone()
                    if self.stoneArr[i][j].STATE.STATE == POSSIBLE_WHITE().STATE:
                        self.stoneArr[i][j].showStone()


    def checkIsPossibleBlack(self, i, j):
        directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0,1], [1, -1], [1, 0], [1,1]]
        
        for i_ in range(8):
            dx = directions[i_][0]
            dy = directions[i_][1]

            x = i + dx
            y = j + dy
            ct = 0

            while x >= 0 and y >=0 and x < 8 and y < 8 and self.stoneArr[x][y].STATE.STATE == WHITE().STATE:
                ct += 1
                x += dx
                y += dy
            
            if x >= 0 and y >=0 and x < 8 and y < 8 and self.stoneArr[x][y].STATE.STATE == BLACK().STATE and ct >0:
                return True

        return False

    def checkIsPossibleWhite(self, i, j):
        directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0,1], [1, -1], [1, 0], [1,1]]
        
        for i_ in range(8):
            dx = directions[i_][0]
            dy = directions[i_][1]

            x = i + dx
            y = j + dy
            ct = 0
            while x >= 0 and y >=0 and x < 8 and y < 8 and self.stoneArr[x][y].STATE.STATE == BLACK().STATE:
                ct += 1
                x += dx
                y += dy
            
            if x >= 0 and y >=0 and x < 8 and y < 8 and self.stoneArr[x][y].STATE.STATE == WHITE().STATE and ct >0:
                return True

        return False

    def flieStones(self, x, y):
        if turn:
            self.stoneArr[x][y].changeState(BLACK())
        else:
            self.stoneArr[x][y].changeState(WHITE())

        directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0,1], [1, -1], [1, 0], [1,1]]
        for i in range(8):
            dx = directions[i][0]
            dy  = directions[i][1]

            x_ = x + dx
            y_ = y + dy

            while x >= 0 and y >=0 and x < 8 and y < 8 and ((self.stoneArr[x_][y_].STATE.STATE == WHITE().STATE and turn) or (self.stoneArr[x_][y_].STATE.STATE == BLACK().STATE and turn == False)):
                if turn:
                    self.stoneArr[x_][y_].changeState(BLACK())
                else:
                    self.stoneArr[x_][y_].changeState(WHITE())
                x_ += dx
                y_ += dy

    def start(self):
        startGame(self.mainScene)

main = MainClass()
main.start()