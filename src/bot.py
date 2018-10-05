from copy import deepcopy


class Bot:
    """The Bot class is the implementation of our bot for the Tetris game.

    There are four key pieces of data that are required by the Bot class:
    height_weight, line_clears_weight, holes_weight and bumpiness_weight
    These weights are used to determine what is the best move possible in
    the current state of the game. By varying these values a different
    effectiveness of the bot is achievable.

    """

    def __init__(self, height_weight, line_clears_weight, holes_weight,
                 bumpiness_weight):
        self.height_weight = height_weight
        self.line_clears_weight = line_clears_weight
        self.holes_weight = holes_weight
        self.bumpiness_weight = bumpiness_weight

    def best(self, grid, tetromino):
        """Find the move with the highest score.

        Uses only the tetromino currently being played.

        """
        best_tetromino = None
        best_score = None

        for i in range(4):
            processed_tetromino = deepcopy(tetromino)
            processed_tetromino.rotations(i)

            while grid.can_move(processed_tetromino, -1):
                processed_tetromino.column -= 1

            while grid.is_valid(processed_tetromino):
                old_row = processed_tetromino.row
                while grid.can_move(processed_tetromino, 0):
                    processed_tetromino.row += 1

                grid.add_tetromino(processed_tetromino)
                score = (-self.height_weight * grid.aggregate_height() +
                         self.line_clears_weight * grid.line_clears() -
                         self.holes_weight * grid.holes() -
                         self.bumpiness_weight * grid.bumpiness())

                grid.remove_tetromino(processed_tetromino)
                processed_tetromino.row = old_row
                if best_score is None or score > best_score:
                    best_score = score
                    best_tetromino = deepcopy(processed_tetromino)

                processed_tetromino.column += 1

        return (best_tetromino, best_score)
