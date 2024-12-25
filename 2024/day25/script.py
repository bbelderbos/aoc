from itertools import product
from pathlib import Path

MAX_SIZE = 5


def solve_part1(data: str) -> int:
    pins, keys = [], []
    grids = data.split("\n\n")
    for grid in grids:
        grid = grid.splitlines()
        is_key = grid[0][0] == "."
        grid = grid[:-1] if is_key else grid[1:]
        k = dict.fromkeys(range(len(grid[0])), 0)
        for row in grid:
            for i, cell in enumerate(row):
                if cell == "#":
                    k[i] += 1
        d = keys if is_key else pins
        d.append(list(k.values()))

    total = 0
    for a, b in product(pins, keys):
        if all(a[i] + b[i] <= MAX_SIZE for i in range(len(a))):
            total += 1
    return total


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = (Path(__file__).parent / "input_small.txt").read_text().strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 3
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 3307

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
