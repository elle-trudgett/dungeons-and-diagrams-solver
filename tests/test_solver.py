import os
from pytest import fixture
from pytest import mark

from solver import Solver


class TestSolver:
    @fixture
    def maze(self) -> str:
        with open(os.path.join("testdata", "input_hard.txt"), "r") as f:
            return f.read()

    def test_solve_simple(self):
        with open(os.path.join("testdata", "input_simple.txt"), "r") as f:
            solver = Solver(f.read())
            assert solver.solve()

    def test_solve_tutorial(self):
        with open(os.path.join("testdata", "input_tutorial.txt"), "r") as f:
            solver = Solver(f.read())
            assert solver.solve()

    @mark.skip
    def test_level_one(self):
        with open(os.path.join("testdata", "input_1_1.txt"), "r") as f:
            solver = Solver(f.read())
            assert solver.solve()

    @mark.skip
    def test_solve_hard(self):
        with open(os.path.join("testdata", "input_hard.txt"), "r") as f:
            solver = Solver(f.read())
            assert solver.solve()
