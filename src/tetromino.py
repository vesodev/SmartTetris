from copy import deepcopy
from math import floor
from random import random


TETROMINOES = {"O": [[4, 4],
                     [4, 4]],
               "T": [[0, 2, 0],
                     [2, 2, 2],
                     [0, 0, 0]],
               "S": [[0, 3, 3],
                     [3, 3, 0],
                     [0, 0, 0]],
               "Z": [[1, 1, 0],
                     [0, 1, 1],
                     [0, 0, 0]],
               "J": [[6, 0, 0],
                     [6, 6, 6],
                     [0, 0, 0]],
               "L": [[0, 0, 5],
                     [5, 5, 5],
                     [0, 0, 0]],
               "I": [[0, 0, 0, 0],
                     [7, 7, 7, 7],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]}


class Tetromino:
    def __init__(self, style):
        self.row = 0
        self.column = 3
        self.dimensions = len(TETROMINOES[style])
        self.cells = deepcopy(TETROMINOES[style])

    def rotate(self):
        if self.dimensions == 2:
            return

        d = self.dimensions
        new_cells = [[] for i in range(d)]
        for row in range(d - 1, -1, -1):
            for column in range(d):
                new_cells[column].append(self.cells[row][column])

        self.cells = new_cells

    def rotations(self, n):
        for _ in range(n):
            self.rotate()


class TetrominoGenerator:
    def __init__(self):
        self.bag = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        self.index = 0
        self.shuffle()

    def shuffle(self):
        current_index = len(self.bag)
        while current_index != 0:
            random_index = floor(random() * current_index)
            current_index -= 1
            t = self.bag[current_index]
            self.bag[current_index] = self.bag[random_index]
            self.bag[random_index] = t

    def next(self):
        if self.index >= len(self.bag):
            self.index = 0
            self.shuffle()

        next_tetromino = Tetromino(self.bag[self.index])
        self.index += 1

        return next_tetromino
