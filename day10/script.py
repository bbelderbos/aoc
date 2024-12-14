from pathlib import Path


def str_to_grid(data: str) -> list[list[int]]:
    return [[int(c) for c in row] for row in data.strip().splitlines()]


def find_paths(grid, x, y, current_value, visited, endpoints):
    """
    Finding all possible paths in grid = DFS algorithm
    """
    rows, cols = len(grid), len(grid[0])

    # out of bounds
    if not (0 <= x < rows and 0 <= y < cols):
        return 0
    if (x, y) in visited:
        return 0
    # each step is +1 in value
    if grid[x][y] != current_value + 1:
        return 0
    # destination reached
    if grid[x][y] == 9:
        endpoints.add((x, y))
        return 1

    visited.add((x, y))

    # 4 possible directions
    paths = (
        find_paths(grid, x + 1, y, grid[x][y], visited, endpoints)
        + find_paths(grid, x - 1, y, grid[x][y], visited, endpoints)
        + find_paths(grid, x, y + 1, grid[x][y], visited, endpoints)
        + find_paths(grid, x, y - 1, grid[x][y], visited, endpoints)
    )

    # backtrack
    visited.remove((x, y))
    return paths


def solve_part1(data: str) -> int:
    grid = str_to_grid(data)
    rows, cols = len(grid), len(grid[0])
    trailhead_scores = []

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == 0:
                endpoints = set()  # endpoints are unique
                find_paths(grid, x, y, -1, set(), endpoints)
                score = len(endpoints)
                trailhead_scores.append(score)

    return sum(trailhead_scores)


def solve_part2(data: str) -> int:
    """Solve part 2 of the problem."""
    grid = str_to_grid(data)
    rows, cols = len(grid), len(grid[0])
    trailhead_scores = []

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == 0:
                # for part 2 we can simply stop using unique
                # endpoints to get all available paths
                score = find_paths(grid, x, y, -1, set(), set())
                trailhead_scores.append(score)

    return sum(trailhead_scores)


def main():
    data = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 36
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 816

    part2_test = solve_part2(data)
    assert part2_test == 81
    part2_result = solve_part2(input_file)
    print(f"Part 2: {part2_result}")
    assert part2_result == 1960


if __name__ == "__main__":
    main()
