from collections import deque
from pathlib import Path


def string_to_grid(data: str) -> list:
    return [list(row) for row in data.split("\n")]


def _find_position(grid, target):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == target:
                return (i, j)
    return None


def bfs(grid, start, end, wall_breaker=False):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()
    queue = deque([(start[0], start[1], 0)])

    while queue:
        x, y, steps = queue.popleft()

        if (x, y) == end:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < rows and 0 <= ny < cols) or (nx, ny) in visited:
                continue

            if grid[nx][ny] == "#":
                continue

            visited.add((nx, ny))
            queue.append((nx, ny, steps + 1))

    return -1


def solve_part1(data: str, min_saving: int = 100) -> int:
    grid = string_to_grid(data)
    start = _find_position(grid, "S")
    end = _find_position(grid, "E")
    baseline = bfs(grid, start, end)
    rows, cols = len(grid), len(grid[0])
    cheats = 0
    # TODO: only break walls that are on the path
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == "#":
                # break the wall
                grid[x][y] = "."
                steps_with_break = bfs(grid, start, end)
                gain = baseline - steps_with_break
                if gain >= min_saving:
                    cheats += 1
                # reset
                grid[x][y] = "#"
    return cheats


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = (Path(__file__).parent / "input_small.txt").read_text().strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data, min_saving=20)
    assert part1_test == 5
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 1381

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
