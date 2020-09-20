from bangtal import *

class ObjectNameList:
    def __init__(self):
        self.doorRightOpen = 'images/문-오른쪽-열림.png'
        self.doorRightClosed = 'images/문-오른쪽-닫힘.png'
        self.doorLeftOpen = 'images/문-왼쪽-열림.png'
        self.doorLeftClosed = 'images/문-왼쪽-닫힘.png'
        self.scene1 = 'images/배경-1.png'
        self.scene2 = 'images/배경-2.png'
        self.switch = 'images/스위치.png'
        self.password = 'images/암호.png'
        self.keypad = 'images/키패드.png'
        self.flowerpot = 'images/화분.png'

class Game:
    def __init__(self):
        self.objectNameList = ObjectNameList()
        self.scene1 = Scene('room1', self.objectNameList.scene1)
        self.scene2 = Scene('room2', self.objectNameList.scene2)
        self.doorRight = Object(self.objectNameList.doorRightClosed)
        self.doorLeft = Object(self.objectNameList.doorLeftClosed)
        self.switch = Object(self.objectNameList.switch)

        self.scene_number = 1
        self.doorRightOpened = False
        self.doorLeftOpened = False
        self.switchClicked = False
        self.hiddenDoorOpened = False

    def setObjects(self):
        self.doorRight.locate(self.scene1, 800, 270)
        self.doorRight.show()
        self.doorLeft.locate(self.scene2, 320, 270)
        self.doorLeft.show()
        self.doorRight.onMouseAction = self.onDoorMouseAction
        self.doorLeft.onMouseAction = self.onDoorMouseAction

        self.switch.locate(self.scene2, 800, 500)
        self.switch.show()
        self.switch.onMouseAction = self.onSwitchMouseAction

        self.doorHidden = Object(self.objectNameList.doorRightClosed)
        self.doorHidden.locate(self.scene2, 1000, 250)
        self.doorHidden.onMouseAction = self.onHiddenDoorMouseAction
        
    def onDoorMouseAction(self, x, y, action):
        if self.scene_number == 1:
            if self.doorRightOpened == False:
                self.doorRight.setImage(self.objectNameList.doorRightOpen)
                self.doorRightOpened = True
            else:
                self.scene_number = 2
                self.scene2.enter()
                
        elif self.scene_number == 2:
            if self.doorLeftOpened == False:
                self.doorLeft.setImage(self.objectNameList.doorLeftOpen)
                self.doorLeftOpened = True
            else:
                self.scene_number = 1
                self.scene1.enter()
    
    def onSwitchMouseAction(self, x, y, action):
       if self.switchClicked == False:
           self.doorHidden.show()
           self.switchClicked = True
       else:
           self.doorHidden.hide()
           self.switchClicked = False

    def onHiddenDoorMouseAction(self, x, y, action):
        if self.hiddenDoorOpened == False:
            self.doorHidden.setImage(self.objectNameList.doorRightOpen)
            self.hiddenDoorOpened = True
        else:
            endGame()

    def run(self):
        startGame(self.scene1)

Game1 = Game()
Game1.setObjects()
Game1.run()