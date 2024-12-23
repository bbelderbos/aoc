from collections import Counter
from functools import cache
from pathlib import Path

ROUNDS = 2_000


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
    total = 0
    for row in data.split("\n"):
        secret = int(row)
        for _ in range(ROUNDS):
            secret = evolve_secret(secret)
        total += secret
    return total


def solve_part2(data: str) -> int:
    buyers = data.split("\n")
    all_windows = Counter()

    for buyer in buyers:
        secret = int(buyer)
        results, diffs = [], []
        seen_sequences = set()

        for i in range(ROUNDS):
            secret = evolve_secret(secret)
            res = int(str(secret)[-1])
            results.append(res)

            diffs.append(0 if i == 0 else res - results[-2])

            if i >= 4:
                window = tuple(diffs[-4:])

                if window not in seen_sequences:
                    all_windows[window] += res
                    seen_sequences.add(window)

    best_sequence = max(all_windows, key=all_windows.get)
    total_bananas = 0

    for buyer in buyers:
        secret = int(buyer)
        results, diffs = [], []

        for i in range(ROUNDS):
            secret = evolve_secret(secret)
            res = int(str(secret)[-1])
            results.append(res)

            diffs.append(0 if i == 0 else res - results[-2])

            if i >= 4:
                window = tuple(diffs[-4:])
                if window == best_sequence:
                    total_bananas += res
                    break

    return total_bananas


def main():
    data = (Path(__file__).parent / "input_small.txt").read_text().strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 37327623
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 13185239446

    data = (Path(__file__).parent / "input_small2.txt").read_text().strip()
    part2_test = solve_part2(data)
    assert part2_test == 23
    part2_result = solve_part2(input_file)
    print(f"Part 2: {part2_result}")
    assert part2_result == 1501


if __name__ == "__main__":
    main()
