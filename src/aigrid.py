import grid


class AiGrid(grid.Grid):
    def __init__(self, rows, columns):
        super(AiGrid, self).__init__(rows, columns)

    def line_clears(self):
        filled_rows = 0
        for row in range(self.rows):
            if self.is_row_filled(row):
                filled_rows += 1

        return filled_rows

    def column_height(self, column):
        current_row = 0
        while current_row < self.rows and self.cells[current_row][column] == 0:
            current_row += 1

        return self.rows - current_row

    def aggregate_height(self):
        sum = 0
        for col in range(self.columns):
            sum += self.column_height(col)

        return sum

    def bumpiness(self):
        sum = 0
        for i in range(self.columns - 1):
            sum += abs(self.column_height(i) - self.column_height(i + 1))

        return sum

    def holes(self):
        count = 0
        for i in range(self.columns):
            is_blocking = False
            for j in range(self.rows):
                if self.cells[j][i] != 0:
                    is_blocking = True
                elif is_blocking:
                    count += 1

        return count
