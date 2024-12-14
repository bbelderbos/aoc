from collections import deque
from pathlib import Path


def create_blocks(data: str) -> list[str]:
    idx = 0
    s = []
    for i, c in enumerate(data):
        d = int(c)
        if i % 2 == 0:  # file
            for _ in range(d):
                s.append(str(idx))
            idx += 1
        else:  # free space
            for _ in range(d):
                s.append(".")
    return s


def calc_checksum(compact: list[int]) -> int:
    return sum(count * digit for count, digit in enumerate(compact))


def backfill(blocks: list[str]) -> list[int]:
    copy = deque(blocks)

    num_dots = blocks.count(".")
    num_digits = len(blocks) - num_dots

    ret = []
    for b in blocks:
        if b == ".":
            while True:
                s = copy.pop()
                if s != ".":
                    break
            digit = int(s)
        else:
            digit = int(b)

        ret.append(digit)

        if len(ret) == num_digits:
            break

    return ret


def solve_part1(data: str) -> int:
    blocks = create_blocks(data)
    compact = backfill(blocks)
    checksum = calc_checksum(compact)
    return checksum


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = """
2333133121414131402
""".strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 1928
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 6421128769094

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
