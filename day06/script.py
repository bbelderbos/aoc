from enum import Enum
from itertools import cycle
from typing import NamedTuple
# from pprint import pp


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


class Position(NamedTuple):
    x: int
    y: int


def parse_grid(grid: str) -> list[list[str]]:
    return [list(row) for row in grid.splitlines()]


def find_in_grid(grid: list[str], target: str = "^") -> Position:
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == target:
                return Position(i, j)
    raise ValueError(f"{target} not found in grid")


directions = cycle([d.value for d in Direction])


def traverse_grid(grid, start: Position | None = None) -> int:
    if start is None:
        start = find_in_grid(grid)

    processed = set()
    direction = next(directions)
    i, j = start
    while True:
        processed.add(Position(i, j))
        next_pos = Position(i + direction[0], j + direction[1])

        # grid[i][j] = "X"
        # pp(grid)

        try:
            if grid[next_pos.x][next_pos.y] == "#":
                direction = next(directions)
                continue
        except IndexError:
            return len(processed)
        i, j = next_pos


if __name__ == "__main__":
    data = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()

    """
    grid = parse_grid(data)
    count = traverse_grid(grid)
    assert count == 41
    """

    with open("input.txt", "r") as f:
        data = f.read()

    grid = parse_grid(data)
    count = traverse_grid(grid)
    assert count == 4758
