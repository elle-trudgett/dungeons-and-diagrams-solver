from pytest import raises
from cell import Cell, CellType


class TestCell:
    def test_initial(self):
        cell = Cell()
        assert not cell.resolved
        assert CellType.FLOOR in cell.candidates
        assert CellType.WALL in cell.candidates
        assert CellType.MONSTER in cell.candidates
        assert CellType.CHEST in cell.candidates

    def test_resolve(self):
        cell = Cell()
        cell.resolve(CellType.WALL)
        assert cell.resolved
        assert cell.contents == CellType.WALL

    def test_eliminate(self):
        cell = Cell()
        cell.eliminate(CellType.MONSTER)
        cell.eliminate(CellType.CHEST)
        assert not cell.resolved
        assert CellType.FLOOR in cell.candidates
        assert CellType.WALL in cell.candidates
        assert CellType.MONSTER not in cell.candidates
        assert CellType.CHEST not in cell.candidates

    def test_cannot_resolve_to_unknown(self):
        cell = Cell()
        with raises(ValueError):
            cell.resolve(CellType.UNKNOWN)

    def test_eliminations_lead_to_resolution(self):
        cell = Cell()
        cell.eliminate(CellType.FLOOR)
        cell.eliminate(CellType.MONSTER)
        cell.eliminate(CellType.CHEST)
        assert cell.resolved
        assert cell.contents == CellType.WALL

    def test_elimination_error(self):
        cell = Cell()
        cell.resolve(CellType.FLOOR)
        cell.eliminate(CellType.MONSTER)  # Shouldn't complain

        with raises(ValueError):
            cell.eliminate(CellType.FLOOR)
