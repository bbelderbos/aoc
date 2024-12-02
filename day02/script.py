from itertools import pairwise

MAX_DELTA = 3


def parse_input(data: str) -> list[list[int]]:
    return [list(map(int, line.split())) for line in data.strip().splitlines()]


def is_safe_report(rows: list[int], max_delta: int = MAX_DELTA) -> bool:
    if len(rows) < 2:
        return True

    is_still_increasing = True
    is_still_decreasing = True

    for a, b in pairwise(rows):
        delta = b - a
        if abs(delta) < 1 or abs(delta) > max_delta:
            return False

        if delta > 0:
            is_still_decreasing = False
        elif delta < 0:
            is_still_increasing = False

    return is_still_increasing or is_still_decreasing


def is_safe_report_with_fault_margin(rows: list[int]) -> bool:
    for i in range(len(rows)):
        rows_with_one_less = rows[:i] + rows[i + 1:]
        if is_safe_report(rows_with_one_less):
            return True
    return False


def solve_part1(data: list[list[int]]) -> int:
    return sum(1 for rows in data if is_safe_report(rows))


def solve_part2(data: list[list[int]]) -> int:
    return sum(1 for rows in data if is_safe_report_with_fault_margin(rows))


def test_examples():
    example_input = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip()
    data = parse_input(example_input)
    assert solve_part1(data) == 2
    assert solve_part2(data) == 4


def main():
    test_examples()

    # results for submission
    with open("input.txt", "r") as f:
        input_data = f.read()
    data = parse_input(input_data)

    part1 = solve_part1(data)
    print(f"Part 1: {part1}")

    part2 = solve_part2(data)
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
