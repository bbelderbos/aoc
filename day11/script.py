from functools import cache
from itertools import chain
from pathlib import Path


@cache
def _transform(inp: int) -> list[int]:
    match inp:
        case 0:
            return [1]
        case x if (s := str(x)).isdigit() and len(s) % 2 == 0:
            mid = len(s) // 2
            return [int(s[:mid]), int(s[mid:])]
        case _:
            return [inp * 2024]


def solve_part1(data: str) -> int:
    stones = [int(x) for x in data.split()]
    num_blinks = 25
    for _ in range(num_blinks):
        stones = list(chain(*map(_transform, stones)))
    return len(stones)


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = "125 17"
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 55312
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 233050

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
