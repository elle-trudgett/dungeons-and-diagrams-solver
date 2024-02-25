import os
from pytest import fixture
from board import Board
from cell import CellType


class TestBoard:
    @fixture
    def board(self) -> Board:
        return Board()

    @fixture
    def maze(self) -> str:
        with open(os.path.join("testdata", "maze.txt"), "r") as f:
            return f.read()

    def test_load(self, board: Board, maze: str):
        board.load(maze)

        assert board.width == 8
        assert board.height == 8

        assert board.get_wall_count(column=0) == 6
        assert board.get_wall_count(row=2) == 5
        cell = board.get_cell(column=2, row=0)

        assert cell.resolved
        assert cell.contents == CellType.MONSTER

        cell = board.get_cell(column=7, row=3)
        assert not cell.resolved

        print(board)
