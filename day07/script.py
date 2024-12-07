from functools import cache
from itertools import product
from operator import add, mul
from pathlib import Path
from typing import Callable, Generator, NamedTuple


class Operation(NamedTuple):
    target_result: int
    operations: list[int]


def parse_data(data: str) -> Generator[Operation, None, None]:
    for row in data.splitlines():
        res, ops = row.split(": ")
        yield Operation(int(res), [int(o) for o in ops.split()])


def solve_part1(data: str, ops: list[Callable] = [add, mul]) -> int:
    """Solve part 1 of the problem."""
    parsed_data = parse_data(data)
    valid = []
    for operation in parsed_data:
        combos = product(ops, repeat=len(operation.operations) - 1)
        for combo in combos:
            result = operation.operations[0]

            for num, op in zip(operation.operations[1:], combo):
                result = op(result, num)

            if result == operation.target_result:
                valid.append(operation.target_result)
                break

    return sum(valid)


@cache
def concat(*args):
    return int("".join(str(a) for a in args))


def solve_part2(data: str) -> int:
    """Solve part 2 of the problem."""
    return solve_part1(data, ops=[add, mul, concat])


def main():
    data = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 3749
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 5837374519342

    part2_test = solve_part2(data)
    assert part2_test == 11387
    part2_result = solve_part2(input_file)
    print(f"Part 2: {part2_result}")
    assert part2_result == 492383931650959


if __name__ == "__main__":
    main()
