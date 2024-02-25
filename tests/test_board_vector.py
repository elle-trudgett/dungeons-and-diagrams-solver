from board_vector import BoardVector
from cell import Cell, CellType


class TestBoardVector:
    def test_vector(self):
        cells = [Cell() for n in range(5)]
        cells[0].resolve(CellType.WALL)
        cells[1].eliminate(CellType.WALL)

        vector = BoardVector(cells=cells, wall_count=3)

        assert vector.wall_count == 3
        assert vector.get_walls_placed() == 1
        assert vector.get_walls_placeable() == 3
