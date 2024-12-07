import sys
from pathlib import Path


def create_aoc_script(day: int):
    day_str = f"day{day:02}"
    script_path = Path(day_str) / "script.py"

    if script_path.exists():
        print(f"Script already exists: {script_path}")
        return

    template_code = """from pathlib import Path


def solve_part1(data: str) -> int:
    \"\"\"Solve part 1 of the problem.\"\"\"


# def solve_part2(data: str) -> int:
#     \"\"\"Solve part 2 of the problem.\"\"\"


def main():
    data = "".strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 0
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 0

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
"""

    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text(template_code)
    print(f"Script created successfully: {script_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_aoc_script.py <day_number>")
        sys.exit(1)

    try:
        day_number = int(sys.argv[1])
        create_aoc_script(day_number)
    except ValueError:
        print("Please provide a valid day number as an integer.")
        sys.exit(1)

