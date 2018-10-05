import grid
from tetromino import Tetromino
import unittest


class TestGrid(unittest.TestCase):
    def test_can_move_down(self):
        g = grid.Grid(22, 10)
        tetromino = Tetromino('I')
        tetromino.rotate()
        tetromino.row = 18
        self.assertFalse(g.can_move(tetromino, 0))
        tetromino.row = 20
        self.assertFalse(g.can_move(tetromino, 0))
        tetromino.row = 17
        self.assertTrue(g.can_move(tetromino, 0))
        tetromino.rotate()
        self.assertTrue(g.can_move(tetromino, 0))
        tetromino.row = 20
        self.assertFalse(g.can_move(tetromino, 0))

    def test_can_move_left(self):
        g = grid.Grid(22, 10)
        tetromino = Tetromino('Z')
        for i in range(18, 22):
            g.cells[i][0] = 3
        g.cells[18][1] = 2
        g.cells[19][1] = 0
        g.cells[20][1] = 3
        g.cells[21][1] = 1
        tetromino.row = 19
        tetromino.column = 2
        self.assertTrue(g.can_move(tetromino, -1))

    def test_can_move_right(self):
        g = grid.Grid(22, 10)
        tetromino = Tetromino('Z')
        for i in range(18, 22):
            g.cells[i][9] = 3
        g.cells[18][8] = 2
        g.cells[19][8] = 0
        g.cells[20][8] = 3
        g.cells[21][8] = 1
        tetromino.row = 18
        tetromino.column = 5
        self.assertTrue(g.can_move(tetromino, 1))

    def test_clear_rows(self):
        g = grid.Grid(8, 10)
        for i in range(4, 8):
            for j in range(10):
                g.cells[i][j] = 1
        g.cells[5][6] = 0
        cleared_lines = g.clear_rows()
        self.assertEqual(cleared_lines, 3)
        current_grid = grid.Grid(8, 10)
        for i in range(10):
            current_grid.cells[7][i] = 1
        current_grid.cells[7][6] = 0
        self.assertEqual(g.cells, current_grid.cells)


if __name__ == '__main__':
    unittest.main()
