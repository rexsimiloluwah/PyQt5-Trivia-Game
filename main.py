import sys
import random
from PyQt5.QtGui import QPixmap 
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QMainWindow,
    QPushButton,
    QDesktopWidget,
    QGridLayout
)

from utils import (
    fetch_categories,
    fetch_questions_local
)

# counter for the quiz (30 seconds)
counter = 30

class TriviaApp(QWidget):
    def __init__(self, width=600, height=500):
        super().__init__()
        self.width = width 
        self.height = height  
        self.SCORE_PER_QUESTION = 5
        self.questions = []
        self.score = 0
        self.index = 0
        self.amount = 40
        self.categories = fetch_categories()
        self.difficulties = ["Easy","Medium", "Hard"]
        self.selectedCategory = 9
        self.selectedDifficulty = 'medium'
        self.timeSeconds = 30
        idx = list(range(40))
        random.shuffle(idx)
        self.questions_idx = idx[:30]
        print(self.questions_idx)

        self.widgets = {
            "playButton": [],
            "settingsButton": [],
            "logo": [],
            "questionCount": [],
            "scoreCount": [],
            "timeCount": [],
            "question": [],
            "optionA": [],
            "optionB": [],
            "optionC": [],
            "optionD": [],
            "endGameHeader": [],
            "endGameScore": [],
            "endGamePlayAgain": [],
            "endGameStatus": [],
            "selectCategoryText": [],
            "selectCategoryComboBox": [],
            "selectDifficultyText": [],
            "selectDifficultyComboBox": [],
            "startQuizButton": []
        }

        self.loadUi()
        self.show()

    def loadUi(self):
        """ Initialize the Main Window's UI """
        self.setWindowTitle("SuperTrivia")
        self.resize(self.width, self.height)
        self.center()

        # Set background color for the main window 
        self.setStyleSheet('background: #A1C7D3;')

        # Working with grids 
        self.grid = QGridLayout()
        self.home()
        self.setLayout(self.grid)

    def home(self):
        # Logo 
        logo = QLabel(self)
        logoImg = QPixmap("images/logo.png")
        logo.setMaximumHeight(64)
        logo.setPixmap(logoImg)
        logo.resize(logoImg.width(), logoImg.height())
        logo.setAlignment(QtCore.Qt.AlignCenter)

        self.widgets["logo"].append(logo)

        # Play Button 
        playButton = QPushButton()
        playButton.setText("Play Quiz")
        playButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        playButton.setStyleSheet(
            "*{background: #4D5FE7;"+
            "color: white;"+
            "border: 2px solid '#000000';"+
            "border-radius: 15px;"+
            "font-size: 18px;"+
            "margin: 0px 128px;"+
            "padding: 10px 24px}"+
            "*:hover{border: none;}"
        )
        self.widgets["playButton"].append(playButton)

        # Attach start game event to playButton
        playButton.clicked.connect(self.on_play)

        settingsButton = QPushButton()
        settingsButton.setText("Settings")
        settingsButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        settingsButton.setStyleSheet(
            "*{background: #FBBB0B;"+
            "color: white;"+
            "border: 2px solid '#000000';"+
            "border-radius: 15px;"+
            "font-size: 18px;"+
            "margin: 0px 128px;"+
            "padding: 10px 24px}"+
            "*:hover{border: none;}"
        )
        self.widgets["settingsButton"].append(settingsButton)

        self.grid.addWidget(self.widgets["logo"][-1], 0, 0,1,2)
        self.grid.addWidget(self.widgets["playButton"][-1], 1, 0,1,2)
        self.grid.addWidget(self.widgets["settingsButton"][-1], 2, 0,1,2)

    def setupGameFrame(self):
        text1 = QLabel("Select Category")
        text1.setMaximumHeight(32)
        text1.setStyleSheet('font-size: 24px;')
        text1.setAlignment(QtCore.Qt.AlignCenter)

        text2 = QLabel("Select Difficulty")
        text2.setMaximumHeight(32)
        text2.setStyleSheet('font-size: 24px;')
        text2.setAlignment(QtCore.Qt.AlignCenter)

        selectCategoryComboBox = QtWidgets.QComboBox(self)
        selectCategoryComboBox.setGeometry(QtCore.QRect(200, 150, 100, 100))
        selectCategoryComboBox.setStyleSheet(
            'height: 30px;'+
            'border: 3px solid #4D5FE7;'
        )
        for (k,v) in self.categories.items():
            selectCategoryComboBox.addItem(k)

        selectDifficultyComboBox = QtWidgets.QComboBox(self)
        selectDifficultyComboBox.setGeometry(QtCore.QRect(200, 150, 100, 100))
        selectDifficultyComboBox.addItems(self.difficulties)
        selectDifficultyComboBox.setStyleSheet(
            'height: 30px;'+
            'border: 3px solid #4D5FE7;'
        )

        selectCategoryComboBox.activated.connect(lambda x: self.setCategory(x))
        selectDifficultyComboBox.activated.connect(lambda x: self.setDifficulty(x))

        startButton = QPushButton()
        startButton.setText("Start Quiz")
        startButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        startButton.setStyleSheet(
            "*{background: #4D5FE7;"+
            "color: white;"+
            "border: 2px solid '#000000';"+
            "border-radius: 15px;"+
            "font-size: 18px;"+
            "margin: 0px 128px;"+
            "padding: 10px 24px}"+
            "*:hover{border: none;}"
        )
        startButton.clicked.connect(self.startQuiz)

        self.widgets["selectCategoryText"].append(text1)
        self.widgets["selectCategoryComboBox"].append(selectCategoryComboBox)
        self.widgets["selectDifficultyText"].append(text2)
        self.widgets["selectDifficultyComboBox"].append(selectDifficultyComboBox)
        self.widgets["startQuizButton"].append(startButton)

        self.grid.addWidget(self.widgets["selectCategoryText"][-1], 0, 0,1,2)
        self.grid.addWidget(self.widgets["selectCategoryComboBox"][-1], 1, 0,1,2)
        self.grid.addWidget(self.widgets["selectDifficultyText"][-1], 2, 0,1,2)
        self.grid.addWidget(self.widgets["selectDifficultyComboBox"][-1], 3, 0,1,2)
        self.grid.addWidget(self.widgets["startQuizButton"][-1], 4, 0, 1,2)

    def setCategory(self, x):
        self.selectedCategory = list(self.categories.values())[x]

    def setDifficulty(self, x):
        self.selectedDifficulty = self.difficulties[x].lower()

    def startQuiz(self):
        self.questions = fetch_questions_local(
            self.selectedCategory,
            self.amount,
            self.selectedDifficulty
        )

        if not self.questions:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setText("Sorry, This Category does not contain any questions yet!")
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Cancel|QtWidgets.QMessageBox.Retry)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)

            msgBox.setInformativeText("Kindly select another category to get started.") # Like a description 
            # A detailed text is hidden initially and can be show by clicking the "Show Details" button 

            x = msgBox.exec_()
        else:
            self.clear_widgets()
            self.triviaFrame()

    def triviaFrame(self):
        """ Layout for the Trivia frame for the main quiz """
        self.current_question = self.questions[self.questions_idx[0]]
        questionCount = QLabel(f"{self.index+1}/{len(self.questions)}")
        questionCount.setMaximumHeight(50)
        questionCount.setAlignment(QtCore.Qt.AlignLeft)
        questionCount.setStyleSheet(
            'font-size: 24px;'+
            'padding: 10px;'+
            'font-weight: bold;'+
            'font-family: Orbitron;'
        )

        scoreCount = QLabel(f"{self.score}/{len(self.questions)*self.SCORE_PER_QUESTION}")
        scoreCount.setMaximumHeight(50)
        scoreCount.setAlignment(QtCore.Qt.AlignRight)
        scoreCount.setStyleSheet(
            'font-size: 24px;'+
            'padding: 10px;'+
            'font-weight: bold;'+
            'font-family: Orbitron;'
        )

        question = QLabel()
        question.setMaximumHeight(150)
        question.setText(self.current_question['question'])
        question.setAlignment(QtCore.Qt.AlignCenter)
        question.setWordWrap(True)  #To ensure that it can fill more than one line
        question.setStyleSheet(
            'font-size: 18px;'
        ) 

        global counter
        self.timeCount = QLabel()
        self.timeCount.setMaximumHeight(30)
        self.timeCount.setAlignment(QtCore.Qt.AlignCenter)
        self.timeCount.setWordWrap(True)
        self.timeCount.setStyleSheet(
            'font-size: 15px;'+
            'padding: 0px;'+
            'font-family: Orbitron;'
        )

        random.shuffle(self.current_question['options'])
        print(self.questions[self.questions_idx[0]]["correct_answer"])
        optionA = self.create_option_button(self.current_question['options'][0])
        optionB = self.create_option_button(self.current_question['options'][1])
        optionC = self.create_option_button(self.current_question['options'][2])
        optionD = self.create_option_button(self.current_question['options'][3])


        self.widgets['questionCount'].append(questionCount)
        self.widgets['scoreCount'].append(scoreCount)
        self.widgets['timeCount'].append(self.timeCount)
        self.widgets['question'].append(question)
        self.widgets['optionA'].append(optionA)
        self.widgets['optionB'].append(optionB)
        self.widgets['optionC'].append(optionC)
        self.widgets['optionD'].append(optionD)

        self.grid.addWidget(self.widgets["timeCount"][-1], 0, 0,1,2)
        self.grid.addWidget(self.widgets['questionCount'][-1], 1, 0)
        self.grid.addWidget(self.widgets['scoreCount'][-1], 1, 1)
        self.grid.addWidget(self.widgets['question'][-1], 2, 0, 1,2) #Extra parameters are for row and column span
        self.grid.addWidget(self.widgets['optionA'][-1], 3, 0)
        self.grid.addWidget(self.widgets['optionB'][-1], 3, 1)
        self.grid.addWidget(self.widgets['optionC'][-1], 4, 0)
        self.grid.addWidget(self.widgets['optionD'][-1], 4, 1)

        ## Timer 
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.lapse)
        self.timer.start(1000)

    def lapse(self):
        global counter
        self.timeCount.setText(f"00:{str(counter)}")
        if counter== 0:
            self.clear_widgets()
            self.endGameFrame()
            counter = 30

        counter -= 1

    def create_option_button(self, text):
        button = QPushButton()
        button.setText(text)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setFixedWidth(300)
        button.setStyleSheet(
            "*{background: #4D5FE7;"+
            "color: white;"+
            "border: 2px solid '#000000';"+
            "border-radius: 15px;"+
            "font-size: 18px;"+
            "padding: 18px;}"
            "*:hover{border: none;}"
        )

        button.clicked.connect(lambda x: self.answer_question(button))
        return button

    def answer_question(self, button):
        if str(self.current_question["correct_answer"]) == str(button.text()):
            print("Correct")
            self.update_question()
        else:
            #print("Incorrect")
            self.clear_widgets()
            self.endGameFrame()

    def update_time_counter(self):
        global counter 
        counter = 30

    def update_question(self):
        """ Update question """
        self.score += self.SCORE_PER_QUESTION
        self.update_time_counter()
        self.widgets["scoreCount"][-1].setText(f"{self.score}/{len(self.questions)*self.SCORE_PER_QUESTION}")
        self.index+= 1
        self.widgets["questionCount"][-1].setText(f"{self.index+1}/{len(self.questions)}")
        self.questions_idx.pop(0)
        self.current_question = self.questions[self.questions_idx[0]]
        print(self.current_question["correct_answer"])
        random.shuffle(self.current_question['options'])
        self.widgets["question"][-1].setText(self.current_question["question"])
        self.widgets["optionA"][0].setText(self.current_question["options"][0])
        self.widgets["optionB"][0].setText(self.current_question["options"][1])
        self.widgets["optionC"][0].setText(self.current_question["options"][2])
        self.widgets["optionD"][0].setText(self.current_question["options"][3])


    def clear_widgets(self):
        """ Clearing the widgets applying LIFO principle (stacks) """
        for widget in self.widgets:
            if len(self.widgets[widget]) != 0:
                self.widgets[widget][-1].hide()
            for _ in range(len(self.widgets[widget])):
                self.widgets[widget].pop()

    def on_play(self):
        self.clear_widgets()
        self.setupGameFrame()

    def endGameFrame(self):
        """ The layout for the end game frame """
        header = QLabel("Your Score")
        header.setStyleSheet(
            "font-size: 32px;"
        )
        header.setMaximumHeight(32)
        header.setAlignment(QtCore.Qt.AlignCenter)
        self.widgets["endGameHeader"].append(header)

        score = QLabel()
        score.setText(str(self.score))
        score.setStyleSheet(
            "font-size: 50px;"+
            "font-weight: bold;"
        )
        score.setMaximumHeight(50)
        score.setAlignment(QtCore.Qt.AlignCenter)
        self.widgets["endGameScore"].append(score)

        playAgainButton = QPushButton("Play Again")
        playAgainButton.setStyleSheet(
            "*{background: #4D5FE7;"+
            "color: white;"+
            "border: 2px solid '#000000';"+
            "border-radius: 15px;"+
            "font-size: 18px;"+
            "margin: 0px 128px;"+
            "padding: 10px 24px}"+
            "*:hover{border: none;}"
        )
        playAgainButton.clicked.connect(self.playAgain)
        self.widgets["endGamePlayAgain"].append(playAgainButton)

        self.grid.addWidget(self.widgets["endGameHeader"][-1], 0, 0,1,2)
        self.grid.addWidget(self.widgets["endGameScore"][-1], 1, 0, 1,2)
        self.grid.addWidget(self.widgets["endGamePlayAgain"][-1], 2, 0,1,2)

    def playAgain(self):
        """ Controls the Play again button event """
        self.score = 0
        self.index = 0
        idx = list(range(40))
        random.shuffle(idx)
        self.questions_idx = idx[:30]
        self.clear_widgets()
        #self.home()
        self.setupGameFrame()


    def center(self):
        """ Automatically center the window """
        qRectangle = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qRectangle.moveCenter(center)
        self.move(qRectangle.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TriviaApp()
    sys.exit(app.exec_())
