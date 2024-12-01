from collections import Counter

def parse_input(input_data):
    col1, col2 = [], []
    for line in input_data.strip().split("\n"):
        num1, num2 = map(int, line.split())
        col1.append(num1)
        col2.append(num2)

    col1.sort()
    col2.sort()
    return col1, col2

def solve_part1(col1, col2):
    return sum(abs(a - b) for a, b in zip(col1, col2))

def solve_part2(col1, col2):
    frequency_map = Counter(col2)
    return sum(num * frequency_map[num] for num in col1)

# Example usage
if __name__ == "__main__":
    example_input = """
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
    """
    col1, col2 = parse_input(example_input)

    part1 = solve_part1(col1, col2)
    print(f"Part 1: {part1}")
    assert part1 == 11, f"Expected 11, got {part1}"

    part2 = solve_part2(col1, col2)
    print(f"Part 2: {part2}")
    assert part2 == 31, f"Expected 31, got {part2}"

    # To test with real input file
    with open("input.txt") as f:
        input_data = f.read()
    col1, col2 = parse_input(input_data)
    print(f"Part 1: {solve_part1(col1, col2)}")
    print(f"Part 2: {solve_part2(col1, col2)}")

