from pathlib import Path
from collections import Counter


def str_to_grid(data: str) -> list[list[str]]:
    return [list(row) for row in data.splitlines()]


def calc_parimeter_for_cell(grid, cell, pos):
    i, j = pos
    total = 0
    """
    rows, cols = len(grid), len(grid[0])
    for x, y in [(i-1, j), (i, j+1), (i+1, j), (i, j-1)]:
        if 0 <= x < rows and 0 <= y < cols and grid[x][y] != cell:
            total += 1
        elif not (0 <= x < rows and 0 <= y < cols):
            total += 1
    """
    for x, y in [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]:
        try:
            if grid[x][y] != cell:
                total += 1
        except IndexError:
            total += 1
    return total


def flood_recursive(grid, start_x, start_y, new_value):
    """
    https://lvngd.com/blog/flood-fill-algorithm-python/
    """
    width = len(grid)
    height = len(grid[0])

    def fill(x, y, start, new_value):
        # if the square is not the same plant as the starting point
        if grid[x][y] != start:
            return
        # if the square is not the new plant
        elif grid[x][y] == new_value:
            return
        else:
            # update the plant of the current square to the replacement plant
            grid[x][y] = new_value
            neighbors = [
                (x - 1, y),
                (x + 1, y),
                (x - 1, y - 1),
                (x + 1, y + 1),
                (x - 1, y + 1),
                (x + 1, y - 1),
                (x, y - 1),
                (x, y + 1),
            ]
            for n in neighbors:
                if 0 <= n[0] <= width - 1 and 0 <= n[1] <= height - 1:
                    fill(n[0], n[1], start, new_value)

    start_cell = grid[start_x][start_y]
    fill(start_x, start_y, start_cell, new_value)
    return grid


def solve_part1(data: str) -> int:
    grid = str_to_grid(data)
    new_value = 0
    area, parimeter = Counter(), Counter()

    # use flood fill to label each cell with a unique value
    # e.g. if there are different regions for plants, so we label them 0, 1, ...
    visited = set()
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if (i, j) in visited:
                continue
            grid = flood_recursive(grid, i, j, new_value)
            new_value += 1
            visited.add((i, j))

    # loop through the updated grid and calculate the area and perimeter for each cell
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            area[cell] += 1
            n = calc_parimeter_for_cell(grid, cell, (i, j))
            parimeter[cell] += n

    return sum(v * parimeter[k] for k, v in area.items())


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    breakpoint()
    assert part1_test == 1930
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result < 1469726

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
