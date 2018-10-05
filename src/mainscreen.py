import game
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QLabel, QLCDNumber,
                             QPushButton, QWidget, QFrame, QApplication)


class MainScreen(QWidget):
    def __init__(self):
        super(MainScreen, self).__init__()

        self.mainGame = game.Game()
        nextTetrominoLabel = QLabel()
        nextTetrominoLabel.setFrameStyle(QFrame.Box | QFrame.Raised)
        nextTetrominoLabel.setAlignment(Qt.AlignCenter)

        levelLcd = QLCDNumber(2)
        levelLcd.setSegmentStyle(QLCDNumber.Filled)
        linesLcd = QLCDNumber(5)
        linesLcd.setSegmentStyle(QLCDNumber.Filled)

        startButton = QPushButton("&Start")
        startButton.setFocusPolicy(Qt.NoFocus)
        botButton = QPushButton("&Activate Bot")
        botButton.setFocusPolicy(Qt.NoFocus)
        pauseButton = QPushButton("&Pause")
        pauseButton.setFocusPolicy(Qt.NoFocus)

        currentGame = self.mainGame
        startButton.clicked.connect(currentGame.start)
        pauseButton.clicked.connect(currentGame.pause)
        botButton.clicked.connect(currentGame.activateBot)
        currentGame.linesClearedChanged.connect(linesLcd.display)
        currentGame.levelChanged.connect(levelLcd.display)
        currentGame.nextTetrominoChanged.connect(nextTetrominoLabel.setPixmap)

        layout = QGridLayout()
        layout.addWidget(self.createLabel("NEXT"), 0, 0)
        layout.addWidget(nextTetrominoLabel, 1, 0)
        layout.addWidget(self.createLabel("LEVEL"), 2, 0)
        layout.addWidget(levelLcd, 3, 0)
        layout.addWidget(startButton, 4, 0)
        layout.addWidget(currentGame, 0, 1, 6, 1)
        layout.addWidget(self.createLabel("LINES CLEARED"), 2, 2)
        layout.addWidget(linesLcd, 3, 2)
        layout.addWidget(botButton, 4, 2)
        layout.addWidget(pauseButton, 5, 2)
        self.setLayout(layout)

        self.setWindowTitle("Tetris")
        self.resize(550, 370)

    def createLabel(self, text):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        return lbl


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainScreen()
    window.show()

    sys.exit(app.exec_())
