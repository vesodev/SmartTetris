class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = [[0 for col in range(columns)] for row in range(rows)]

    def is_row_filled(self, row):
        for column in range(self.columns):
            if self.cells[row][column] == 0:
                return False

        return True

    def is_row_empty(self, row):
        for column in range(self.columns):
            if self.cells[row][column] != 0:
                return False

        return True

    def exceeded(self):
        return not self.is_row_empty(0) or not self.is_row_empty(1)

    def add_tetromino(self, tetromino):
        for i in range(tetromino.dimensions):
            for j in range(tetromino.dimensions):
                row = tetromino.row + i
                column = tetromino.column + j
                if tetromino.cells[i][j] != 0 and row >= 0:
                    self.cells[row][column] = tetromino.cells[i][j]

    def remove_tetromino(self, tetromino):
        for i in range(tetromino.dimensions):
            for j in range(tetromino.dimensions):
                row = tetromino.row + i
                column = tetromino.column + j
                if tetromino.cells[i][j] != 0:
                    self.cells[row][column] = 0

    def is_valid(self, tetromino):
        for i in range(tetromino.dimensions):
            for j in range(tetromino.dimensions):
                row = tetromino.row + i
                column = tetromino.column + j
                if tetromino.cells[i][j] != 0:
                    if (column < 0 or column >= self.columns or
                       row < 0 or row >= self.rows or
                       self.cells[row][column] != 0):
                        return False

        return True

    def can_move(self, tetromino, direction):
        for i in range(tetromino.dimensions):
            for j in range(tetromino.dimensions):
                row = tetromino.row + i + (0 if direction else 1)
                column = tetromino.column + j + direction
                if tetromino.cells[i][j] != 0:
                    if (column < 0 or column >= self.columns or
                       row < 0 or row >= self.rows or
                       self.cells[row][column] != 0):
                        return False

        return True

    def clear_rows(self):
        dist = 0
        for row in range(self.rows - 1, -1, -1):
            if self.is_row_filled(row):
                dist += 1
                for column in range(self.columns):
                    self.cells[row][column] = 0
            elif dist > 0:
                for column in range(self.columns):
                    self.cells[row + dist][column] = self.cells[row][column]
                    self.cells[row][column] = 0

        return dist

    def reset(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.cells[row][col] = 0
