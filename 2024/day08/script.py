from collections import defaultdict
from math import gcd
from pathlib import Path


def parse_map(grid):
    antennas = defaultdict(list)
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char not in ".#":
                antennas[char].append((x, y))
    return antennas


def find_antinodes(antennas, width, height):
    antinodes = set()

    for freq, positions in antennas.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # calculate the distance between the two antennas
                dx, dy = x2 - x1, y2 - y1

                # antinodes in both directions
                antinode1 = (x1 - dx, y1 - dy)
                antinode2 = (x2 + dx, y2 + dy)

                # only add antinodes that are within the grid
                if 0 <= antinode1[0] < width and 0 <= antinode1[1] < height:
                    antinodes.add(antinode1)
                if 0 <= antinode2[0] < width and 0 <= antinode2[1] < height:
                    antinodes.add(antinode2)

    return antinodes


def find_antinodes_part2(antennas, width, height):
    antinodes = set()

    for freq, positions in antennas.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # calculate the distance between the two antennas
                dx, dy = x2 - x1, y2 - y1

                # take the lowest common multiple of dx and dy
                step = gcd(dx, dy)
                step_x, step_y = dx // step, dy // step

                # now we have to fill the whole grid line with antinodes

                # step backwards
                cur_x, cur_y = x1, y1
                while 0 <= cur_x < width and 0 <= cur_y < height:
                    antinodes.add((cur_x, cur_y))
                    cur_x -= step_x
                    cur_y -= step_y

                # step forwards
                cur_x, cur_y = x1 + step_x, y1 + step_y
                while 0 <= cur_x < width and 0 <= cur_y < height:
                    antinodes.add((cur_x, cur_y))
                    cur_x += step_x
                    cur_y += step_y

    return antinodes


def solve_part1(data: str) -> int:
    grid = [list(row) for row in data.splitlines()]
    width, height = len(grid[0]), len(grid)
    antennas = parse_map(grid)
    antinodes = find_antinodes(antennas, width, height)
    return len(antinodes)


def solve_part2(data: str) -> int:
    grid = [list(row) for row in data.splitlines()]
    width, height = len(grid[0]), len(grid)
    antennas = parse_map(grid)
    antinodes = find_antinodes_part2(antennas, width, height)
    return len(antinodes)


def main():
    data = """
......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
""".strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 14
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 423

    part2_test = solve_part2(data)
    assert part2_test == 34
    part2_result = solve_part2(input_file)
    print(f"Part 2: {part2_result}")
    assert part2_result == 1287


if __name__ == "__main__":
    main()
