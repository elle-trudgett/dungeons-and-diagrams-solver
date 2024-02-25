from typing import Optional

from board import Board


class Solver:
    board: Board

    def __init__(self, maze):
        self.board = Board()
        self.board.load(maze)

    def solve(self) -> Board:
        """
        Returns the solution, as a :class:`Board`.
        """

        if self._is_solved():
            return self.board
        else:
            raise ValueError("No solution was found")

    def _is_solved(self):
        for row in range(self.board.height):
            for column in range(self.board.width):
                if not self.board.get_cell(column=column, row=row).resolved:
                    return False
        return True
