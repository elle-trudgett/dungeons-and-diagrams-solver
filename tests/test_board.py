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
        with open(os.path.join("testdata", "input_hard.txt"), "r") as f:
            return f.read()

    def load_solved(self, filename: str) -> Board:
        with open(os.path.join("testdata", filename), "r") as f:
            board = Board()
            board.load(f.read())
            for c in board.enumerate_cells():
                if len(c.candidates) == 2:
                    c.resolve(CellType.FLOOR)
            return board

    def test_load(self, board: Board, maze: str):
        board.load(maze)

        assert board.width == 8
        assert board.height == 8

        assert board.get_wall_count(column=1) == 6
        assert board.get_wall_count(row=2) == 5
        cell = board.get_cell(column=3, row=0)

        assert cell.resolved
        assert cell.contents == CellType.MONSTER

        cell = board.get_cell(column=7, row=3)
        assert not cell.resolved

    def test_get_row(self, board: Board, maze: str):
        board.load(maze)
        row = board.get_row(7)
        assert len(row) == 8
        assert row[3].contents == CellType.MONSTER

    def test_get_column(self, board: Board, maze: str):
        board.load(maze)
        column = board.get_column(0)
        assert len(column) == 8
        assert column[0].contents == CellType.MONSTER
        assert column[4].contents == CellType.MONSTER
        assert column[6].contents == CellType.MONSTER

    def test_reload(self):
        solved_board = self.load_solved("valid.txt")
        assert solved_board.get_cell(column=0, row=0).contents == CellType.WALL
        solved_board.get_cell(column=0, row=0).resolve(CellType.FLOOR)
        assert solved_board.get_cell(column=0, row=0).contents == CellType.FLOOR
        solved_board.reload()
        assert solved_board.get_cell(column=0, row=0).contents == CellType.WALL

    def test_is_valid(self):
        assert self.load_solved("valid.txt").is_valid()
        assert self.load_solved("unknown_wall_count.txt").is_valid()
        assert self.load_solved("monster_no_deadend_unknown.txt").is_valid()

        assert not self.load_solved("invalid_wall_count.txt").is_valid()
        assert not self.load_solved("non_contiguous.txt").is_valid()
        assert not self.load_solved("deadend_no_monster.txt").is_valid()
        assert not self.load_solved("monster_no_deadend.txt").is_valid()

    def test_is_valid_with_unknowns(self):
        assert self.load_solved("incomplete.txt").is_valid()
