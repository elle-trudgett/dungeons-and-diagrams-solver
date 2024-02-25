from dataclasses import dataclass

from cell import Cell, CellType


@dataclass
class BoardVector:
    cells: list[Cell]
    wall_count: int

    def get_walls_placed(self):
        return len([c for c in self.cells if c.contents == CellType.WALL])

    def get_walls_placeable(self):
        return len([c for c in self.cells if not c.resolved and CellType.WALL in c.candidates])
