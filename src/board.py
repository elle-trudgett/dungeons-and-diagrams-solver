import re
from typing import Iterator

from board_vector import BoardVector
from cell import Cell, CellType


class Board:
    height: int
    width: int
    wall_counts_rows: list[int]
    wall_counts_columns: list[int]
    cells: list[list[Cell]]
    source: str
    comment: ""

    def __init__(self):
        self.height = 0
        self.width = 0
        self.wall_counts_rows = []
        self.wall_counts_columns = []
        self.cells = []
        self.comment = ""

    def load(self, maze: str) -> None:
        self.source = maze

        self.height = 0
        self.width = 0
        self.wall_counts_rows = []
        self.wall_counts_columns = []
        self.cells = []
        self.comment = ""

        for line in maze.split("\n"):
            orig_line = line
            line = re.sub(r'\s', '', line)
            if not line:
                continue
            if line.startswith("//"):
                self.comment = orig_line.strip()[2:].strip()
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
                    elif c == "#":
                        new_cell.resolve(CellType.WALL)
                    elif c == "_":
                        new_cell.eliminate(CellType.MONSTER)
                        new_cell.eliminate(CellType.CHEST)
                    elif c == "?":
                        pass  # leave as unresolved
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

    def enumerate_cells(self) -> Iterator[Cell]:
        for row in self.cells:
            for cell in row:
                yield cell

    def __str__(self) -> str:
        output = "┌───┬" + "──" * self.width + "─┐\n"
        output += "│ * │ "
        for i in range(self.width):
            output += f"{self.wall_counts_columns[i]} "
        output += "│\n"
        output += "├───┼" + "──" * self.width + "─┤\n"
        for r in range(self.height):
            output += f"│ {self.wall_counts_rows[r]} │ "
            for c in self.cells[r]:
                output += f"{c} "
            output += "│\n"
        output += "└───┴" + "──" * self.width + "─┘\n"

        return output[:-1]

    def __repr__(self) -> str:
        return f"Board('{self.comment or self.id}')"

    def get_row(self, row: int):
        return self.cells[row]

    def get_column(self, column: int):
        return [
            row[column] for row in self.cells
        ]

    def enumerate_vectors(self) -> Iterator[BoardVector]:
        """
        Enumerate all rows and columns
        """
        for r in range(self.height):
            row = self.get_row(r)
            wall_count = self.get_wall_count(row=r)
            yield BoardVector(cells=row, wall_count=wall_count)
        for c in range(self.width):
            col = self.get_column(c)
            wall_count = self.get_wall_count(column=c)
            yield BoardVector(cells=col, wall_count=wall_count)

    def get_neighbors(self, *, column, row) -> list[Cell]:
        neighbors = []
        if row > 0:  # Up
            neighbors.append(self.get_cell(column=column, row=row - 1))
        if row < self.height - 1:  # Down
            neighbors.append(self.get_cell(column=column, row=row + 1))
        if column > 0:  # Left
            neighbors.append(self.get_cell(column=column - 1, row=row))
        if column < self.width - 1:  # Right
            neighbors.append(self.get_cell(column=column + 1, row=row))
        return neighbors

    def is_valid(self) -> bool:
        for v in self.enumerate_vectors():
            if v.get_walls_placed() > v.wall_count or v.get_walls_placed() + v.get_walls_placeable() < v.wall_count:
                # Wall count constraint not satisfied
                print("INVALID (wcc):")
                print(self)
                return False

        for r, row in enumerate(self.cells):
            for c, cell in enumerate(row):
                if cell.contents == CellType.FLOOR:
                    # Ensure no floor is surrounded by N-1 walls (deadend with
                    # no monster) -- where N is the number of adjacencies
                    neighbors = self.get_neighbors(column=c, row=r)

                    walls_around_cell = len([c for c in neighbors if c.contents == CellType.WALL])
                    if walls_around_cell >= len(neighbors) - 1:
                        print("INVALID (dnm):")
                        print(self)
                        return False
                elif cell.contents == CellType.MONSTER:
                    # Ensure monsters have exactly one floor neighbor
                    neighbors = self.get_neighbors(column=c, row=r)
                    floors_around_cell = len([n for n in neighbors if n.contents == CellType.FLOOR])
                    if floors_around_cell > 1:
                        print("INVALID (mnd):")
                        print(self)
                        return False
                    if floors_around_cell == 0:
                        # If no floor is found, and there's no chance for a floor to be found
                        if all([n.resolved for n in neighbors]):
                            print("INVALID (mnd):")
                            print(self)
                            return False

        # Contiguity check:
        # Number of non-wall spaces should be == the number of spaces
        # accessible from any one blank space
        non_walls = [c for c in self.enumerate_cells() if c.contents != CellType.WALL]
        if non_walls:
            non_walls_reachable = self._non_walls_reachable()
            if non_walls_reachable != len(non_walls):
                print("INVALID (nc):")
                print(self)
                return False

        return True

    def _non_walls_reachable(self) -> int:
        for r, row in enumerate(self.cells):
            for c, cell in enumerate(row):
                if cell.contents != CellType.WALL:
                    reachable_from = self._non_walls_reachable_from(row=r, column=c, visited=[])
                    return reachable_from
        return 0

    def _non_walls_reachable_from(self, *, row, column, visited) -> int:
        """
        Calculate the number of non-wall spaces that are reachable from this cell,
        including the current cell
        :return:
        """
        this_cell = self.get_cell(row=row, column=column)
        if this_cell in visited:
            return 0
        visited.append(this_cell)

        if this_cell.contents == CellType.WALL:
            return 0

        # Up
        if row > 0:
            reachable_up = self._non_walls_reachable_from(row=row - 1, column=column, visited=visited)
        else:
            reachable_up = 0

        # Down
        if row < self.height - 1:
            reachable_down = self._non_walls_reachable_from(row=row + 1, column=column, visited=visited)
        else:
            reachable_down = 0

        # Left
        if column > 0:
            reachable_left = self._non_walls_reachable_from(row=row, column=column - 1, visited=visited)
        else:
            reachable_left = 0

        # Right
        if column < self.width - 1:
            reachable_right = self._non_walls_reachable_from(row=row, column=column + 1, visited=visited)
        else:
            reachable_right = 0

        return 1 + reachable_up + reachable_down + reachable_left + reachable_right

    def reload(self):
        self.load(self.source)
