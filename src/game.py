from PyQt5.QtCore import pyqtSignal, QBasicTimer, QSize, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QFrame
from copy import deepcopy
import tetromino
import aigrid
from bot import Bot


COLOR_TABLE = [0x000000, 0xf00000, 0xa000f0, 0x00f000,
               0xf0f000, 0xf0a000, 0x0000f0, 0x00f0f0]


class Game(QFrame):
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 22

    linesClearedChanged = pyqtSignal(int)
    levelChanged = pyqtSignal(int)
    nextTetrominoChanged = pyqtSignal(QPixmap)

    def __init__(self):
        super(Game, self).__init__()
        self.board = aigrid.AiGrid(Game.BOARD_HEIGHT, Game.BOARD_WIDTH)
        self.bot = Bot(0.520162, 0.771727, 0.36483, 0.183434)
        self._tetrominoGenerator = tetromino.TetrominoGenerator()
        self.currentTetromino = None
        self.nextTetromino = None
        self.linesCleared = 0
        self.level = 1
        self.isBotActive = False
        self.isStarted = False
        self.isPaused = False
        self.isGameOver = False

        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setFocusPolicy(Qt.StrongFocus)
        self.timer = QBasicTimer()
        self.linesClearedChanged.connect(self._increaseLevel)

    def timeoutTime(self):
        return 1000 / (1 + self.level)

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.isGameOver = False
        self.isBotActive = False
        self.linesCleared = 0
        self.level = 0
        self.currentTetromino = self._tetrominoGenerator.next()
        self.nextTetromino = self._tetrominoGenerator.next()
        self.board.reset()
        self.board.add_tetromino(self.currentTetromino)

        self.linesClearedChanged.emit(self.linesCleared)
        self.nextTetrominoChanged.emit(self._nextTetrominoPixmap())
        self.update()

    def pause(self):
        if not self.isStarted or self.isGameOver:
            return

        self.isPaused = not self.isPaused
        if self.isPaused:
            self.timer.stop()
        else:
            if self.isBotActive:
                self.timer.start(10, self)
            else:
                self.timer.start(self.timeoutTime(), self)

        self.update()

    def activateBot(self):
        if self.isPaused or not self.isStarted:
            return

        self.isBotActive = not self.isBotActive
        if self.isBotActive:
            self.timer.start(10, self)
            self._drop()
        else:
            self.timer.start(self.timeoutTime(), self)
        self.update()

    def squareWidth(self):
        return self.contentsRect().width() / Game.BOARD_WIDTH

    def squareHeight(self):
        return self.contentsRect().height() / Game.BOARD_HEIGHT

    def sizeHint(self):
        return QSize(Game.BOARD_WIDTH * 15 + self.frameWidth() * 2,
                     Game.BOARD_HEIGHT * 15 + self.frameWidth() * 2)

    def minimumSizeHint(self):
        return QSize(Game.BOARD_WIDTH * 5 + self.frameWidth() * 2,
                     Game.BOARD_HEIGHT * 5 + self.frameWidth() * 2)

    def paintEvent(self, event):
        super(Game, self).paintEvent(event)

        painter = QPainter(self)
        rect = self.contentsRect()

        if self.isPaused:
            painter.drawText(rect, Qt.AlignCenter, "Pause")
            return
        elif self.isGameOver:
            painter.drawText(rect, Qt.AlignCenter, "Game Over")
            return

        boardTop = rect.bottom() - Game.BOARD_HEIGHT * self.squareHeight()
        cells = self.board.cells
        for i in range(Game.BOARD_HEIGHT):
            for j in range(Game.BOARD_WIDTH):
                if cells[i][j] != 0:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(),
                                    cells[i][j])

    def drawSquare(self, painter, x, y, squareType):
        color = QColor(COLOR_TABLE[squareType])

        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1,
                         y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,
                         y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + 1)

    def _nextTetrominoPixmap(self):
        d = self.nextTetromino.dimensions
        pixmap = QPixmap(d * self.squareWidth(),
                         d * self.squareHeight())
        painter = QPainter(pixmap)
        painter.fillRect(pixmap.rect(), self.palette().window())
        rect = pixmap.rect()
        cells = self.nextTetromino.cells
        for i in range(d):
            for j in range(d):
                if cells[i][j] != 0:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    rect.top() + i * self.squareHeight(),
                                    cells[i][j])

        painter.end()
        return pixmap

    def keyPressEvent(self, event):
        if (not self.isStarted or self.isPaused or self.isGameOver or
           self.isBotActive):
            super(Game, self).keyPressEvent(event)
            return

        key = event.key()
        if key == Qt.Key_Left:
            self._tryMove(-1)
        elif key == Qt.Key_Right:
            self._tryMove(1)
        elif key == Qt.Key_Down:
            self._applyGravity()
        elif key == Qt.Key_Up:
            self._rotate()
        elif key == Qt.Key_Space:
            self._drop()
        else:
            super(Game, self).keyPressEvent(event)

    def bot_move(self):
        self.currentTetromino = self.bot.best(self.board,
                                              self.currentTetromino)[0]

    def _applyGravity(self):
        self.board.remove_tetromino(self.currentTetromino)
        if self.board.can_move(self.currentTetromino, 0):
            self.currentTetromino.row += 1
            self.board.add_tetromino(self.currentTetromino)
        else:
            self._setCurrentTetromino()

        self.update()

    def _tryMove(self, direction):
        self.board.remove_tetromino(self.currentTetromino)
        if self.board.can_move(self.currentTetromino, direction):
            self.currentTetromino.column += direction
        self.board.add_tetromino(self.currentTetromino)
        self.update()

    def _increaseLevel(self, clearedLines):
        if clearedLines % 45 == 0:
            self.level += 1
            if not self.isBotActive:
                self.timer.start(self.timeoutTime(), self)
            self.levelChanged.emit(self.level)

    def _setCurrentTetromino(self):
        self.board.add_tetromino(self.currentTetromino)
        cleared_rows = self.board.clear_rows()
        if cleared_rows:
            self.linesCleared += cleared_rows
            self.linesClearedChanged.emit(self.linesCleared)
        if not self.board.exceeded():
            self.currentTetromino = self.nextTetromino
            if self.isBotActive:
                self.bot_move()
            self.board.add_tetromino(self.currentTetromino)
            self.nextTetromino = self._tetrominoGenerator.next()
            self.nextTetrominoChanged.emit(self._nextTetrominoPixmap())
        else:
            self.isGameOver = True
            self.timer.stop()
        self.update()

    def _rotate(self):
        clone = deepcopy(self.currentTetromino)
        clone.rotate()
        self.board.remove_tetromino(self.currentTetromino)
        if self.board.is_valid(clone):
            self.currentTetromino = clone

        self.board.add_tetromino(self.currentTetromino)
        self.update()

    def _drop(self):
        self.board.remove_tetromino(self.currentTetromino)
        while self.board.can_move(self.currentTetromino, 0):
            self.currentTetromino.row += 1
        self._setCurrentTetromino()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self._applyGravity()
        else:
            super(Game, self).timerEvent(event)
