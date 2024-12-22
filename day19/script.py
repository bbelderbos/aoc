from functools import cache
from pathlib import Path


def parse_data(data: str):
    patterns, designs = data.split("\n\n")
    patterns = patterns.split(", ")
    designs = designs.splitlines()
    return patterns, designs


@cache
def can_create_design(words, target):
    # base case: empty string = can always be created
    if target == "":
        return True

    for word in words:
        if target.startswith(word):
            remainder = target.removeprefix(word)
            if can_create_design(words, remainder):
                return True

    return False


@cache
def get_all_designs(words, target):
    total = 0

    if target == "":
        return 1

    for word in words:
        if target.startswith(word):
            remainder = target.removeprefix(word)
            options = get_all_designs(words, remainder)
            total += options

    return total


def can_create_design_iterative(patterns, target):
    stack = [target]
    visited = set()

    while stack:
        current = stack.pop()

        if current == "":
            return True

        if current in visited:
            continue
        visited.add(current)

        for word in patterns:
            if current.startswith(word):
                remainder = current[len(word) :]
                stack.append(remainder)

    return False


def solve_part1(data: str, iteration_over_recursion=False) -> int:
    patterns, designs = parse_data(data)
    patterns = tuple(patterns)
    count = 0
    for design in designs:
        if iteration_over_recursion:
            can_create = can_create_design_iterative(patterns, design)
        else:
            can_create = can_create_design(patterns, design)
        if can_create:
            count += 1
    return count


def solve_part2(data: str) -> int:
    patterns, designs = parse_data(data)
    patterns = tuple(patterns)
    return sum(get_all_designs(patterns, design) for design in designs)


def main():
    data = (Path(__file__).parent / "input_small.txt").read_text().strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    part1_test_it = solve_part1(data, iteration_over_recursion=True)
    assert part1_test == part1_test_it == 6, part1_test
    part1_result = solve_part1(input_file)
    part1_result_it = solve_part1(input_file, iteration_over_recursion=True)
    print(f"Part 1: {part1_result}")
    assert part1_result == part1_result_it == 304

    part2_test = solve_part2(data)
    assert part2_test == 16
    part2_result = solve_part2(input_file)
    print(f"Part 2: {part2_result}")
    assert part2_result == 705756472327497


if __name__ == "__main__":
    main()
