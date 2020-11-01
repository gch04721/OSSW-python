from bangtal import *
from model import MainModel

class User1:
    def __init__(self, model):
        self.model = model
        self.model.computer = self

    def myTurn(self):
        maxNum = 0
        if not self.model.blackTurn:
            for key, val in self.model.possibleWhiteNum.items():
                if val > maxNum:
                    self.point2Click = key
                    maxNum = val
                    
        self.model.stoneArr[self.point2Click[0]][self.point2Click[1]].userClicked()

class MainView:
    def __init__(self):
        self.mainScene = Scene('main', 'images/background.png')
        self.board = Object('images/board.png')
        self.board.locate(self.mainScene, 40, 40)
        #self.board.show()
        self.model = MainModel(self, 8, 8)
        
        self.black_num1 = Object('images/L0.png')
        self.black_num1.locate(self.mainScene, 750, 225)
        self.black_num2 = Object('images/L0.png')
        self.black_num2.locate(self.mainScene, 825, 225)

        self.white_num1 = Object('images/L0.png')
        self.white_num1.locate(self.mainScene, 1075, 225)
        self.white_num2 = Object('images/L0.png')
        self.white_num2.locate(self.mainScene, 1150, 225)

        self.updateStoneNum()
        
    def start(self):
        self.user = User1(self.model)
        startGame(self.mainScene)

    def updateStoneNum(self):
        black_1 = int(self.model.blackStoneNum / 10)
        if black_1 == 0:
            self.setDigit(self.black_num1, black_1)
        else:
            self.setDigit(self.black_num1, black_1, True)
        black_2 = int(self.model.blackStoneNum % 10)
        self.setDigit(self.black_num2, black_2, True)

        white_1 = int(self.model.whiteStoneNum / 10)
        if white_1 == 0:
            self.white_num2.locate(self.mainScene, 1075, 225)
            self.setDigit(self.white_num1, white_1)
        else:
            self.white_num2.locate(self.mainScene, 1150, 225)
            self.setDigit(self.white_num1, white_1, True)
        white_2 = int(self.model.whiteStoneNum % 10)
        self.setDigit(self.white_num2, white_2, True)

        
            
    def setDigit(self, obj, num, show = False):
        fileDir = 'images/L' + str(num) + '.png'
        obj.setImage(fileDir)
        if show:
            obj.show()
        else:
            obj.hide()

    def gameEnd(self, isBlackWin):
        if isBlackWin:
            showMessage("Black Win")
        else:
            showMessage("White Win")

main = MainView()
main.start()