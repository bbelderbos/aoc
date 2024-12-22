from functools import cache
from pathlib import Path


def _mix(secret: int, result: int) -> int:
    return secret ^ result


def _prune(secret: int) -> int:
    return secret % 16777216


@cache
def evolve_secret(secret: int) -> int:
    result = secret * 64
    secret = _mix(secret, result)
    secret = _prune(secret)
    result = secret // 32
    secret = _mix(secret, result)
    secret = _prune(secret)
    result = secret * 2048
    secret = _mix(secret, result)
    secret = _prune(secret)
    return secret


def solve_part1(data: str) -> int:
    """Solve part 1 of the problem."""
    total = 0
    for row in data.split("\n"):
        secret = int(row)
        for _ in range(2000):
            secret = evolve_secret(secret)
        total += secret
    return total


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = (Path(__file__).parent / "input_small.txt").read_text().strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 37327623
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 13185239446

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
