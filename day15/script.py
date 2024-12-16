from dataclasses import dataclass
from pathlib import Path

MOVES = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


@dataclass
class Position:
    r: int
    c: int
    value: str


def print_grid(grid: list[list[int]]) -> None:
    for row in grid:
        print(" | ".join(str(cell) for cell in row))
    print()


def _find_robot(grid: list[list[str]], char: str = "@"):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == char:
                return r, c


def _calc_value_boxes(grid: list[list[str]]) -> int:
    total = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "O":
                total += r * 100 + c
    return total


def solve_part1(data: str) -> int:
    grid_str, instructions_str = data.split("\n\n")
    grid = [list(row) for row in grid_str.splitlines()]

    instructions = list(instructions_str.replace("\n", ""))
    pos = _find_robot(grid)

    for instruction in instructions:
        # print(instruction)
        move = MOVES[instruction]

        line = []
        r, c = pos
        while 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            line.append(Position(r, c, grid[r][c]))
            r += move[0]
            c += move[1]

        all_chars = [p.value for p in line]
        wall = all_chars.index("#")

        if "." not in all_chars[:wall]:
            # print_grid(grid)
            continue
        if line[1].value == "#":
            # print_grid(grid)
            continue
        if line[1].value == ".":  # move just the bot
            grid[pos[0]][pos[1]] = "."
            grid[line[1].r][line[1].c] = "@"
            pos = line[1].r, line[1].c
            # print_grid(grid)
            continue
        # move O and @ 1 pos
        for i, box in enumerate(line[1:], start=1):
            if box.value in "O.":
                grid[box.r][box.c] = line[i - 1].value
                if box.value == ".":
                    break
        # move the bot
        grid[pos[0]][pos[1]] = "."
        grid[line[1].r][line[1].c] = "@"

        # print_grid(grid)
        pos = line[1].r, line[1].c

    # find boxes
    return _calc_value_boxes(grid)


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""".strip()

    data2 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip()

    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 2028

    part1_test = solve_part1(data2)
    assert part1_test == 10092

    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 1465523

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
