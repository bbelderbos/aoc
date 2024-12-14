from collections import deque
from itertools import chain
from pathlib import Path
from typing import Iterable


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


def calc_checksum(compact: Iterable[int | str]) -> int:
    return sum(
        count * int(digit)
        for count, digit in enumerate(compact)
        if digit != "."
    )


def backfill_part1(blocks: list[str]) -> list[int]:
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


def chunkify(blocks: list[str]) -> list[list[str]]:
    files = []
    file: list[str] = []
    last_file = "0"
    for b in blocks:
        if b != last_file:
            files.append(file)
            file = []
            last_file = b
        file.append(b)
    files.append(file)
    return files


def backfill_part2(blocks: list[str]) -> Iterable[str]:
    chunks = chunkify(blocks)
    copy = chunks.copy()
    while True:
        try:
            chunk = chunks.pop()
        except IndexError:
            break
        index = copy.index(chunk)
        if "." in chunk:
            continue
        for i, c in enumerate(chunks):
            if "." not in c:
                continue
            if len(chunk) <= c.count("."):
                start = c.index(".")
                end = start + len(chunk)
                copy[i][start:end] = chunk
                copy[index] = ["."] * len(chunk)
                break

    return chain(*copy)


def solve_part1(data: str) -> int:
    blocks = create_blocks(data)
    compact = backfill_part1(blocks)
    checksum = calc_checksum(compact)
    return checksum


def solve_part2(data: str) -> int:
    """Solve part 2 of the problem."""
    blocks = create_blocks(data)
    compact = backfill_part2(blocks)
    checksum = calc_checksum(compact)
    return checksum


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

    part2_test = solve_part2(data)
    assert part2_test == 2858
    part2_result = solve_part2(input_file)
    print(f"Part 2: {part2_result}")
    assert part2_result == 6448168620520


if __name__ == "__main__":
    main()
