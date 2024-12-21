import heapq
from pathlib import Path

START_POS = "S"
END_POS = "E"
START_DIRECTION = "right"


def _find_position(grid, target):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == target:
                return (i, j)
    return None


def calculate_cheapest_route(grid, start=None, end=None) -> int:
    if start is None:
        start = _find_position(grid, START_POS)
    if end is None:
        end = _find_position(grid, END_POS)

    rows, cols = len(grid), len(grid[0])
    directions = {"up": (-1, 0), "left": (0, -1), "down": (1, 0), "right": (0, 1)}

    pq = [(0, start[0], start[1], START_DIRECTION)]
    visited = set()

    while pq:
        cost, x, y, current_dir = heapq.heappop(pq)

        if (x, y) == end:
            return cost

        if (x, y, current_dir) in visited:
            continue
        visited.add((x, y, current_dir))

        for new_dir, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != "#":
                # turn is the move + turn cost = 1 + 1k
                move_cost = 1 if new_dir == current_dir else 1001
                new_cost = cost + move_cost
                heapq.heappush(pq, (new_cost, nx, ny, new_dir))

    return -1


def string_to_grid(data: str) -> list:
    return [list(row) for row in data.split("\n")]


def solve_part1(data: str) -> int:
    grid = string_to_grid(data)
    return calculate_cheapest_route(grid)


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = (Path(__file__).parent / "input_small.txt").read_text().strip()
    data2 = (Path(__file__).parent / "input_small2.txt").read_text().strip()
    part1_test = solve_part1(data)
    assert part1_test == 7036
    part1_test = solve_part1(data2)
    assert part1_test == 11048

    input_file = (Path(__file__).parent / "input.txt").read_text().strip()
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 105496

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
