from enum import Enum
from typing import List, Set


class CellType(Enum):
    UNKNOWN = 0
    FLOOR = 1
    WALL = 2
    MONSTER = 3
    CHEST = 4


class Cell:
    """
    Represents one tile in the dungeon.
    """
    resolved: bool
    contents: CellType
    candidates: Set[CellType]

    def __init__(self):
        self.contents = CellType.UNKNOWN
        self.resolved = False
        self.candidates = {CellType.FLOOR, CellType.WALL, CellType.MONSTER, CellType.CHEST}

    def resolve(self, cell_type: CellType) -> None:
        """
        Marks the cell as only containing the particular cell type.
        :param cell_type: The cell type to set this cell to.
        """
        if cell_type == CellType.UNKNOWN:
            raise ValueError("Cannot resolve cell to unknown.")
        self.candidates = {cell_type}
        self.contents = cell_type
        self.resolved = True

    def eliminate(self, cell_type: CellType) -> None:
        """
        Removes from the possible candidates of what this cell could be.
        :param cell_type: The type to remove.
        """
        if cell_type in self.candidates:
            self.candidates.remove(cell_type)

        if not self.candidates:
            raise ValueError("All candidates were removed, this cell has no possibilities.")

        if len(self.candidates) == 1:
            self.resolve(next(iter(self.candidates)))

    def __str__(self) -> str:
        if not self.resolved:
            return "?"
        match self.contents:
            case CellType.WALL: return "#"
            case CellType.FLOOR: return "_"
            case CellType.MONSTER: return "m"
            case CellType.CHEST: return "c"

    def __repr__(self) -> str:
        return f"Cell({self.__str__()})"
