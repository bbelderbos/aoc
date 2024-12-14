from collections import Counter
from functools import cache
from itertools import chain
from pathlib import Path


@cache
def _transform(inp: int) -> list[int]:
    match inp:
        case 0:
            return [1]
        case x if len(s := str(x)) % 2 == 0:
            mid = len(s) // 2
            return [int(s[:mid]), int(s[mid:])]
        case _:
            return [inp * 2024]


def solve_part1(data: str) -> int:
    stones = [int(x) for x in data.split()]
    for _ in range(25):
        stones = list(chain(*map(_transform, stones)))
    return len(stones)


def solve_part2(data: str) -> int:
    stones = Counter(int(x) for x in data.split())

    for _ in range(75):
        next_stones: Counter[int] = Counter()
        for stone, count in stones.items():
            transformed = _transform(stone)
            for new_stone in transformed:
                next_stones[new_stone] += count
        stones = next_stones

    return sum(stones.values())


def main():
    data = "125 17"
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 55312
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 233050

    part2_test = solve_part2(data)
    assert part2_test == 65601038650482
    part2_result = solve_part2(input_file)
    print(f"Part 2: {part2_result}")
    assert part2_result == 276661131175807


if __name__ == "__main__":
    main()
