import tetromino
import unittest


class TestTetromino(unittest.TestCase):
    def test_rotate_I(self):
        t = tetromino.Tetromino('I')
        t.rotate()
        expected = [[0, 0, 7, 0],
                    [0, 0, 7, 0],
                    [0, 0, 7, 0],
                    [0, 0, 7, 0]]
        self.assertEqual(t.cells, expected)
        expected = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [7, 7, 7, 7],
                    [0, 0, 0, 0]]
        t.rotate()
        self.assertEqual(t.cells, expected)
        expected = [[0, 7, 0, 0],
                    [0, 7, 0, 0],
                    [0, 7, 0, 0],
                    [0, 7, 0, 0]]
        t.rotate()
        self.assertEqual(t.cells, expected)
        expected = [[0, 0, 0, 0],
                    [7, 7, 7, 7],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]
        t.rotate()
        self.assertEqual(t.cells, expected)

    def test_rotate_L(self):
        t = tetromino.Tetromino('L')
        expected = [[0, 5, 0],
                    [0, 5, 0],
                    [0, 5, 5]]
        t.rotate()
        self.assertEqual(t.cells, expected)
        expected = [[0, 0, 0],
                    [5, 5, 5],
                    [5, 0, 0]]
        t.rotate()
        self.assertEqual(t.cells, expected)
        expected = [[5, 5, 0],
                    [0, 5, 0],
                    [0, 5, 0]]
        t.rotate()
        self.assertEqual(t.cells, expected)
        expected = [[0, 0, 5],
                    [5, 5, 5],
                    [0, 0, 0]]
        t.rotate()
        self.assertEqual(t.cells, expected)

    def test_rotate_Z(self):
        t = tetromino.Tetromino('Z')
        t.rotate()
        expected = [[0, 0, 1],
                    [0, 1, 1],
                    [0, 1, 0]]
        self.assertEqual(t.cells, expected)
        expected = [[0, 0, 0],
                    [1, 1, 0],
                    [0, 1, 1]]
        t.rotate()
        self.assertEqual(t.cells, expected)
        expected = [[0, 1, 0],
                    [1, 1, 0],
                    [1, 0, 0]]
        t.rotate()
        self.assertEqual(t.cells, expected)
        t.rotate()
        p = tetromino.Tetromino('Z')
        self.assertEqual(t.cells, p.cells)


class TestTetrominoGenerator(unittest.TestCase):
    def test_shuffle(self):
        for _ in range(10):
            generator = tetromino.TetrominoGenerator()
            prev = tetromino.deepcopy(generator.bag)
            generator.shuffle()
            self.assertNotEqual(prev, generator.bag)


if __name__ == '__main__':
    unittest.main()
