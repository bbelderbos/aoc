from enum import Enum
from itertools import cycle
from typing import NamedTuple
from pathlib import Path
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


def find_in_grid(grid: list[list[str]], target: str = "^") -> Position:
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == target:
                return Position(i, j)
    raise ValueError(f"{target} not found in grid")


def traverse_grid(grid: list[list[str]], start: Position) -> set[Position]:
    directions = cycle([d.value for d in Direction])
    direction = next(directions)

    i, j = start
    processed = set()

    while True:
        processed.add(Position(i, j))
        next_pos = Position(i + direction[0], j + direction[1])

        try:
            if grid[next_pos.x][next_pos.y] in ("#", "O"):
                direction = next(directions)
                continue
        except IndexError:
            return processed

        i, j = next_pos


def check_infinite_loop(grid: list[list[str]], start: Position) -> bool:
    directions = cycle([d.value for d in Direction])
    direction = next(directions)

    #pp(grid)
    i, j = start
    visited_states = set()

    while True:
        current_state = (Position(i, j), direction)
        if current_state in visited_states:
            return True  # A true infinite loop is detected
        visited_states.add(current_state)

        next_pos = Position(i + direction[0], j + direction[1])

        try:
            if grid[next_pos.x][next_pos.y] in ("#", "O"):
                direction = next(directions)
                continue
        except IndexError:
            return False  # The guard exits the grid, so no loop

        i, j = next_pos



def solve_part1(data: str) -> int:
    grid = parse_grid(data)
    start = find_in_grid(grid)
    processed = traverse_grid(grid, start)
    return len(processed)


def solve_part2(data: str) -> int:
    grid = parse_grid(data)
    start = find_in_grid(grid)
    processed = traverse_grid(grid, start)
    block_positions = 0

    for cell in processed:
        # Skip the starting position and non-traversable positions
        if grid[cell.x][cell.y] != ".":
            continue

        # Place an obstruction and test
        original_value = grid[cell.x][cell.y]
        grid[cell.x][cell.y] = "O"

        # Check if the obstruction creates a new loop
        if check_infinite_loop(grid, start):
            block_positions += 1

        # Revert the obstruction
        grid[cell.x][cell.y] = original_value

    return block_positions



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

    # Part 1
    part1_test = solve_part1(data)
    assert part1_test == 41
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 4758

    # Part 2
    part2_test = solve_part2(data)
    assert part2_test == 6, f"{part2_test} is not 6"
    part2_result = solve_part2(input_file)
    print(f"Part 2: {part2_result}")
    assert part2_result == 0


if __name__ == "__main__":
    main()

