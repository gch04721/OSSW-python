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
        self.cabinetOpen = 'images/cabinet_open.png'
        self.cabinetClose = 'images/cabinet_close.png'
        self.books = 'images/Books.png'
        self.book_open = 'images/Book_open.png'
        self.desk = 'images/Desk.png'
        self.kitchen = 'images/Kitchen.png'
        self.waterPurifier = "images/water_purifier.png"
        self.key = 'images/열쇠.png'
        self.quiz = 'images/Quiz.jpg'

SceneChange = False

class Scene1:
    def __init__(self):
        self.obj = ObjectNameList()
        self.scene1 = Scene('room1',  self.obj.scene1)
        self.scene1.onEnter = self.onScene1EnterAction
        self.doorRight = Object(self.obj.doorRightClosed)
        self.doorRight.onMouseAction = self.onDoorMouseAction
        self.cabinet = Object(self.obj.cabinetClose)
        self.cabinet.onMouseAction = self.onCabinetMouseAction
        self.books = Object(self.obj.books)
        self.books.onMouseAction = self.onBooksMouseAction
        self.books.onKeypad = self.onBooksKeypad
        self.book_open = Object(self.obj.book_open)
        self.desk = Object(self.obj.desk)
        self.desk.onMouseAction = self.onDeskMouseAction

        self.scene2 = Scene('room2', self.obj.scene2)
        self.scene2.onEnter = self.onScene2EnterAction
        self.kitchen = Object(self.obj.kitchen)
        self.flowerpot = Object(self.obj.flowerpot)
        self.flowerpot.onMouseAction = self.onFlowerpotMouseAction
        self.waterPurifier = Object(self.obj.waterPurifier)
        self.waterPurifier.onMouseAction = self.onWaterpurifierMouseAction
        self.key = Object(self.obj.key)
        self.key.onMouseAction = self.onKeyMouseAction
        self.doorLeft = Object(self.obj.doorLeftClosed)
        self.doorLeft.onMouseAction = self.onDoorLeftMouseAction

        self.quizPass = False
        self.isDoorOpen = False
        self.isCabinetOpen = False
        self.isBookOnDesk = False
        self.isFlowerpotClicked = False

        self.setObject()
    def resetScene1(self):
        self.quizPass = False
        self.isDoorOpen = False
        self.isCabinetOpen = False
        self.isBookOnDesk = False

        self.cabinet.setImage(self.obj.cabinetClose)
        self.doorRight.setImage(self.obj.doorRightClosed)
        self.books.setImage(self.obj.books)
        self.books.locate(self.scene1,60, 130)
        self.books.setScale(0.2)
        self.books.hide()

    def setObject(self):
        self.doorRight.locate(self.scene1, 525, 320)
        self.doorRight.show()

        self.cabinet.locate(self.scene1, 0,110)
        self.cabinet.setScale(0.3)
        self.cabinet.show()

        self.desk.locate(self.scene1, 900, 180)
        self.desk.setScale(0.5)
        self.desk.show()

        self.books.locate(self.scene1,60, 130)
        self.books.setScale(0.2)

        """ scene 2 """
        self.kitchen.locate(self.scene2, 190, 160)
        self.kitchen.setScale(2.0)
        self.kitchen.show()

        self.doorLeft.locate(self.scene2, 10,210)
        self.doorLeft.show()

        self.flowerpot.locate(self.scene2, 900, 200)
        self.flowerpot.show()

        self.key.locate(self.scene2, 320,400)
        self.key.setScale(0.1)
        self.key.show()

        self.waterPurifier.locate(self.scene2, 300,400)
        self.waterPurifier.setScale(0.13)
        self.waterPurifier.show()

    def start(self):
        startGame(self.scene1)

    def doorOpen(self):
        self.doorRight.setImage(self.obj.doorRightOpen)

    def cabinetOpen(self):
        self.cabinet.setImage(self.obj.cabinetOpen)
       
    def cabinetClose(self):
        self.cabinet.setImage(self.obj.cabinetClose)

    def onDoorMouseAction(self, x, y, action):
        if self.isDoorOpen:
            self.scene2.enter()
        else:
            if self.quizPass:
                self.doorOpen()
                self.isDoorOpen = True
            else:
                showMessage("시험공부안하고 어디갈라고!! 얼른 공부해!")

    def onCabinetMouseAction(self, x, y, action):
        if self.isCabinetOpen:
            self.cabinetClose()
            self.isCabinetOpen = False
            self.books.hide()
        else:
            if self.isBookOnDesk:
                self.cabinetOpen()
            else:
                self.cabinetOpen()
                self.books.show()
            self.isCabinetOpen = True

    def onDeskMouseAction(self, x, y, action):
        if self.books.inHand():
            self.books.drop()
            self.books.locate(self.scene1, 1000,350)
            self.books.setScale(0.1)
            self.books.show()
            self.isBookOnDesk = True
        else:
            if self.isBookOnDesk:
                pass
            else:
                showMessage('책부터 가져오자')
    
    def onBooksMouseAction(self, x, y, action):
        if self.isBookOnDesk :
            self.quiz()
        else:
            self.books.setImage(self.obj.book_open)
            self.books.pick()

    def onBooksKeypad(self):
        self.quizTimer.stop()
        showMessage("더 공부하긴 싫다...거실로 나가서 상황을 살펴보자")
        self.quizPass = True
        hideTimer()

    def quiz(self):
        # set Quiz animation
        self.quizTimer = Timer(3.0)
        def timeout2():
            showMessage("공부가 부족하다 더 하고 오자.")
            self.resetScene1()

        def timeout():
            self.quizTimer.set(10.0)
            self.quizTimer.onTimeout = timeout2
            self.quizTimer.start()
            showTimer(self.quizTimer)
            showMessage("a와 b의 값을 차례대로 입력하세요(각 2자리)")
            showKeypad("8282", self.books)

        self.quizTimer.onTimeout = timeout
        self.quizTimer.start()
        showImageViewer(self.obj.quiz)
        

    def onScene1EnterAction(self):
        if self.isFlowerpotClicked:
            showMessage("탈출하다 걸렸다. 처음부터 다시 시작하자")


    def onScene2EnterAction(self):
        question = Timer(2.0)
        def timeout3():
            showMessage("네 알겠습니다.")

        def timeout2():
            question.set(2.0)
            question.start()
            showMessage("얼른 마시고 들어가서 공부해라")
            question.onTimeout = timeout3

        def timeout1():
            question.set(2.0)
            question.start()
            showMessage("물마시려구요")
            question.onTimeout = timeout2
        
        question.start()
        question.onTimeout = timeout1
        showMessage("공부해야지 왜 나왔어??")

   
    def onFlowerpotMouseAction(self, x, y, action):
        showMessage("물만마신다면서? 어서 들어가!")
        self.resetScene1()
        self.scene1.enter()

    def onWaterpurifierMouseAction(self,x,y,action):
        if self.key.inHand():
            pass
        else:
            showMessage("'열쇠가 여기에 있었네..얼른 나가자'")
            self.key.pick()

    def onKeyMouseAction(self, x, y, action):
        pass

    def onDoorLeftMouseAction(self, x, y, action):
        if self.key.inHand():
            showMessage("탈출 성공! 신나게 놀다오세요~")
        else:
            showMessage("물만 마신다더니 뭐하니? 어서 공부하러 들어가!")
    
test = Scene1()
test.start()