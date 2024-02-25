from cell import Cell, CellType


class Board:
    height: int
    width: int
    wall_counts_rows: list[int]
    wall_counts_columns: list[int]
    cells: list[list[Cell]]

    def __init__(self):
        self.height = 0
        self.width = 0
        self.wall_counts_rows = []
        self.wall_counts_columns = []
        self.cells = []

    def load(self, maze: str) -> None:
        for line in maze.split("\n"):
            line = line.strip()
            if line.startswith("//"):
                continue
            if line.startswith("*"):
                self.wall_counts_columns = [int(c) for c in line[1:]]
            elif line[0] in "0123456789":
                self.wall_counts_rows.append(int(line[0]))
                new_row = []
                for c in line[1:]:
                    new_cell = Cell()
                    if c == "m":
                        new_cell.resolve(CellType.MONSTER)
                    elif c == "c":
                        new_cell.resolve(CellType.CHEST)
                    elif c == "_":
                        new_cell.eliminate(CellType.MONSTER)
                        new_cell.eliminate(CellType.CHEST)
                    else:
                        raise ValueError(f"Unexpected character for cell in input: {c}")
                    new_row.append(new_cell)
                self.cells.append(new_row)
            else:
                raise ValueError(f"Unexpected input: {line}")

        self.width = len(self.wall_counts_columns)
        self.height = len(self.wall_counts_rows)

    def get_wall_count(self, *, row: int = None, column: int = None) -> int:
        if row is None and column is None:
            raise ValueError("Can only get wall count for a row or column, not both")
        if row is not None:
            return self.wall_counts_rows[row]
        return self.wall_counts_columns[column]

    def get_cell(self, *, column: int, row: int) -> Cell:
        return self.cells[row][column]

    def __str__(self) -> str:
        return "\n".join([
            "".join([
                cell.__str__() for cell in row
            ]) for row in self.cells
        ])
