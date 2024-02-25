from copy import deepcopy

from board import Board
from board_vector import BoardVector
from cell import CellType


class NoSolutionError(Exception):
    def __init__(self):
        super().__init__("No solutions found")


class Solver:
    board: Board

    def __init__(self, maze):
        self.board = Board()
        self.board.load(maze)

    def solve(self) -> Board:
        """
        Returns the solution, as a :class:`Board`.
        """

        solving = True
        while solving:
            if not self.board.is_valid():
                raise NoSolutionError()
            if self._is_resolved() and self.board.is_valid():
                # Solved
                solving = False
                break
            # Apply rules until no resolutions are made from
            # easier to more complex
            if self._resolve_wall_counts():
                print("Resolved wall counts!")
                print(self.board)
                continue
            if self._resolve_floor_in_front_of_monsters():
                print("Resolved floor in front of monsters!")
                print(self.board)
                continue
            if self._resolve_walls_around_monsters():
                print("Resolved walls around monsters!")
                print(self.board)
                continue
            if self._resolve_dead_ends_with_no_monsters():
                print("Resolved dead ends with no monsters!")
                print(self.board)
                continue
            if self._try_most_constrained():
                continue
            solving = False

        if self._is_resolved() and self.board.is_valid():
            return self.board
        else:
            raise NoSolutionError()

    def _is_resolved(self):
        for row in range(self.board.height):
            for column in range(self.board.width):
                if not self.board.get_cell(column=column, row=row).resolved:
                    return False
        return True

    def _resolve_wall_counts(self) -> bool:
        """
        Goes through and finds rows/columns where the wall count is equal to the number of
        walls placed, or the difference between the two is equal to the number of cells left
        that walls could go.

        :return: true if any cell was resolved, false otherwise
        """
        resolved_a_cell = False

        for v in self.board.enumerate_vectors():
            resolved_a_cell |= self._resolve_wall_count_single(v)

        return resolved_a_cell

    def _resolve_wall_count_single(self, v: BoardVector) -> bool:
        """
        Resolves cells in a list of cells based on the given wall count expected.
        :param cells: List of cells to check
        :param wall_count: Number of walls expected in this list of cells
        :return: True if any cell was resolved
        """

        resolved_cells = False

        if v.wall_count == v.get_walls_placed():
            # All walls are placed, the rest resolve to FLOOR.
            for cell in v.cells:
                if not cell.resolved:
                    cell.resolve(CellType.FLOOR)
                    resolved_cells = True
        elif v.wall_count - v.get_walls_placed() == v.get_walls_placeable():
            # The remaining unknown cells are all WALLs.
            for cell in v.cells:
                if not cell.resolved:
                    cell.resolve(CellType.WALL)
                    resolved_cells = True
        return resolved_cells

    def _try_most_constrained(self) -> bool:
        print("Warning --- I'm trying random stuff now!")
        backup = deepcopy(self.board)

        for r in range(self.board.height):
            for c in range(self.board.width):
                cell = self.board.get_cell(column=c, row=r)
                if cell.resolved:
                    continue
                cell.resolve(CellType.WALL)
                try:
                    self.solve()
                    if self.board.is_valid():
                        return True
                except NoSolutionError:
                    pass  # No biggie, keep trying

                # we messed up, restore
                print(" --- Reverting and trying something else ---")
                self.board = deepcopy(backup)
                print(self.board)

        return False

    def _resolve_floor_in_front_of_monsters(self):
        """
        When all but one of a monster's neighbors are walls, the remaining
        cell must be floor
        """
        resolved = False
        for r in range(self.board.height):
            row = self.board.get_row(r)
            for c in range(self.board.width):
                cell = row[c]
                if cell.contents == CellType.MONSTER:
                    non_wall_neighbors = [n for n in self.board.get_neighbors(column=c, row=r) if n.contents != CellType.WALL]
                    if len(non_wall_neighbors) == 1:
                        non_wall_neighbor = non_wall_neighbors[0]
                        if not non_wall_neighbor.resolved:
                            non_wall_neighbor.resolve(CellType.FLOOR)
                            resolved = True
        return resolved

    def _resolve_walls_around_monsters(self):
        """
        When there is a floor in front of a monsters, all of its other neighbors must be walls
        """
        resolved = False
        for r in range(self.board.height):
            row = self.board.get_row(r)
            for c in range(self.board.width):
                cell = row[c]
                if cell.contents == CellType.MONSTER:
                    neighbors = self.board.get_neighbors(column=c, row=r)
                    floor_neighbors = len([n for n in neighbors if n.contents == CellType.FLOOR])
                    if floor_neighbors == 1:
                        # All other neighbors are walls
                        for n in neighbors:
                            if n.contents == CellType.FLOOR:
                                continue
                            if not n.resolved:
                                n.resolve(CellType.WALL)
                                resolved = True
                    elif floor_neighbors > 1:
                        raise ValueError(f"Invalid state!\n\n{self.board}")

        return resolved

    def _resolve_dead_ends_with_no_monsters(self):
        """
        If an unknown cell is at a dead end, it cannot be a floor
        """
        resolved = False
        for r in range(self.board.height):
            row = self.board.get_row(r)
            for c in range(self.board.width):
                cell = row[c]
                if not cell.resolved:
                    neighbors = self.board.get_neighbors(column=c, row=r)
                    wall_neighbors = len([n for n in neighbors if n.contents == CellType.WALL])

                    if wall_neighbors == len(neighbors) - 1:
                        cell.resolve(CellType.WALL)
                        resolved = True
        return resolved


TEST_MAZE = """
// The Shifting Walls
* 6 2 4 3 4 4 2 6
6 _ _ m _ m _ _ _
2 _ _ _ _ _ _ _ _
5 _ _ _ _ _ _ _ m
3 m _ _ _ _ _ _ _
2 _ _ _ _ _ _ _ m
5 m _ _ _ _ _ _ _
2 _ _ _ _ _ _ _ _
6 _ _ _ m _ m _ _"""

if __name__ == "__main__":
    solver = Solver(TEST_MAZE)

    print("Problem:")
    print(solver.board)

    print()

    print("Solution:")
    print(solver.solve())
