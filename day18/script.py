from collections import deque
from pathlib import Path


def create_grid(x=70, y=70):
    grid = []
    for i in range(y):
        grid.append(["." for j in range(x)])
    return grid


def fill_grid(grid, coords):
    for i, coord in enumerate(coords):
        x, y = int(coord[0]), int(coord[1])
        grid[y][x] = "#"
    return grid


def print_grid(grid):
    for row in grid:
        print(" ".join(row))


def shortest_path(grid, start=None, end=None):
    rows, cols = len(grid), len(grid[0])
    if start is None:
        start = (0, 0)
    if end is None:
        end = (rows - 1, cols - 1)

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    queue = deque([(start[0], start[1], 0)])
    visited = set()
    visited.add(start)

    while queue:
        x, y, steps = queue.popleft()
        if (x, y) == end:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < rows
                and 0 <= ny < cols
                and (nx, ny) not in visited
                and grid[nx][ny] == "."
            ):
                queue.append((nx, ny, steps + 1))
                visited.add((nx, ny))

    return -1


def solve_part1(data: str, grid_size: int, num_bytes: int) -> int:
    coords = [row.split(",") for row in data.splitlines()]
    grid = create_grid(x=grid_size, y=grid_size)
    grid = fill_grid(grid, coords[:num_bytes])
    return shortest_path(grid)


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = (Path(__file__).parent / "input_small.txt").read_text().strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data, grid_size=7, num_bytes=12)
    assert part1_test == 22
    part1_result = solve_part1(input_file, grid_size=71, num_bytes=1024)
    print(f"Part 1: {part1_result}")
    assert part1_result == 282

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
