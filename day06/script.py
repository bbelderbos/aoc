from enum import Enum
from itertools import cycle
from typing import NamedTuple
from pathlib import Path


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


def traverse_grid(grid, start: Position | None = None) -> int:
    if start is None:
        start = find_in_grid(grid)

    directions = cycle([d.value for d in Direction])
    direction = next(directions)

    i, j = start
    processed = set()

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


def solve_part1(data: str) -> int:
    grid = parse_grid(data)
    return traverse_grid(grid)


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
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
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 41
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 4758

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
