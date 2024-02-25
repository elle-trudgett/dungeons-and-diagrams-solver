import os
from pytest import fixture

from solver import Solver


class TestSolver:
    @fixture
    def maze(self) -> str:
        with open(os.path.join("testdata", "maze.txt"), "r") as f:
            return f.read()

    def test_solve(self, maze):
        solver = Solver(maze)
        solution = solver.solve()

        assert solution
