from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

NUM_SECONDS = 100
TREE_BASE_THRESHOLD = 10


class Position(NamedTuple):
    x: int
    y: int


class Speed(NamedTuple):
    x: int
    y: int


@dataclass
class Robot:
    speed: Speed
    start: Position
    current: Position

    def move(self, grid_x: int, grid_y: int) -> None:
        new_x = (self.current.x + self.speed.x) % grid_x
        new_y = (self.current.y + self.speed.y) % grid_y
        self.current = Position(new_x, new_y)


def create_grid(x: int, y: int, fill: int = 0) -> list[list[int]]:
    return [[fill for _ in range(x)] for _ in range(y)]


def print_grid(grid: list[list[int]]) -> None:
    for row in grid:
        print(" | ".join(str(cell) for cell in row))
    print()


def parse_robots(data: str) -> list[Robot]:
    robots = []
    for line in data.strip().splitlines():
        p, v = line.split(" ")
        pp = p.split("=")[1].split(",")
        vv = v.split("=")[1].split(",")

        speed = Speed(x=int(vv[0]), y=int(vv[1]))
        start = Position(x=int(pp[0]), y=int(pp[1]))

        robot = Robot(speed, start, start)
        robots.append(robot)
    return robots


def solve_part1(data: str, x: int, y: int) -> int:
    """Solve part 1 of the problem."""
    grid = create_grid(x, y)
    for robot in parse_robots(data):
        for _ in range(NUM_SECONDS):
            robot.move(x, y)
        grid[robot.current.y][robot.current.x] += 1

    mid_row = y // 2
    mid_col = x // 2

    # exclude middle row and middle column
    quadrant_1 = [row[:mid_col] for row in grid[:mid_row]]
    quadrant_2 = [row[mid_col + 1 :] for row in grid[:mid_row]]
    quadrant_3 = [row[:mid_col] for row in grid[mid_row + 1 :]]
    quadrant_4 = [row[mid_col + 1 :] for row in grid[mid_row + 1 :]]

    q1_sum = sum(c for row in quadrant_1 for c in row)
    q2_sum = sum(c for row in quadrant_2 for c in row)
    q3_sum = sum(c for row in quadrant_3 for c in row)
    q4_sum = sum(c for row in quadrant_4 for c in row)

    return q1_sum * q2_sum * q3_sum * q4_sum


def _longest_consecutive(nums: list[int]) -> int:
    max_streak = 0
    current_streak = 0

    for i in range(len(nums)):
        if i == 0 or nums[i] == nums[i - 1] + 1:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1

    return max_streak


def solve_part2(data: str, x: int, y: int) -> int:
    robots = parse_robots(data)

    active_rows: defaultdict[int, list[int]] = defaultdict(list)

    for second in range(1, 1_000_001):
        active_rows.clear()

        for robot in robots:
            robot.move(x, y)
            row = robot.current.y
            col = robot.current.x

            active_rows[row].append(col)

        for row, positions in active_rows.items():
            positions.sort()  # sort to find consecutive robots
            max_consecutive = _longest_consecutive(positions)
            if max_consecutive > TREE_BASE_THRESHOLD:
                print(f"Row {row} has {max_consecutive} consecutive robots.")
                return second

    return -1


def main():
    data = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data, 11, 7)
    assert part1_test == 12
    part1_result = solve_part1(input_file, 101, 103)
    print(f"Part 1: {part1_result}")
    assert part1_result == 229069152

    part2_result = solve_part2(input_file, 101, 103)
    print(f"Part 2: {part2_result}")
    assert part2_result == 7383


if __name__ == "__main__":
    main()
