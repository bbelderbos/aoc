from pathlib import Path
from collections import Counter, defaultdict


class Grid:
    def __init__(self, data: str):
        self.grid = self._str_to_grid(data)
        self._new_value = 0
        self._regions: dict[int, list] = {}
        self._area: Counter = Counter()
        self._perimeter: Counter = Counter()

    def _str_to_grid(self, data: str) -> list[list[str]]:
        return [list(row) for row in data.splitlines()]

    def _calc_perimeter_for_cell(self, cell: str, pos: tuple[int, int]) -> int:
        i, j = pos
        total = 0
        for x, y in [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]:
            try:
                if self.grid[x][y] != cell:
                    total += 1
            except IndexError:
                total += 1
        return total

    def calc_area_and_perimeter(self) -> int:
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                cell = self.grid[i][j]
                self._area[cell] += 1
                self._perimeter[cell] += self._calc_perimeter_for_cell(cell, (i, j))
        return sum(
            self._area[region] * self._perimeter[region]
            for region in self._regions.keys()
        )

    def _count_sides(self, cells):
        cells_set = set(cells)
        vertical_sides, horizontal_sides = defaultdict(list), defaultdict(list)

        for x, y in cells:
            for x2, y2 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                # filters out internal edges
                if (x2, y2) not in cells_set:
                    if x2 != x:
                        vertical_sides[(x, x2)].append(y)
                    else:
                        horizontal_sides[(y, y2)].append(x)

        ret = 0
        for sides in list(vertical_sides.values()) + list(horizontal_sides.values()):
            sides.sort()
            ret += (
                sum([1 for i in range(len(sides) - 1) if sides[i + 1] - sides[i] > 1])
                + 1
            )

        return ret

    def calc_cost_of_sides(self) -> int:
        total = 0
        for region, cells in self._regions.items():
            total += len(cells) * self._count_sides(cells)
        return total

    def uniquify_regions(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                # skip cells that are already labeled
                if str(self.grid[i][j]).isdigit():
                    continue
                cells = self._flood_recursive(i, j, self._new_value)
                self._regions[self._new_value] = cells
                self._new_value += 1

    def _flood_recursive(
        self, start_x: int, start_y: int, new_value: int
    ) -> list[tuple[int, int]]:
        """
        Perform flood fill starting at (start_x, start_y) and replace the region
        with `new_value`.
        Good example: https://lvngd.com/blog/flood-fill-algorithm-python/
        """
        width = len(self.grid)
        height = len(self.grid[0])
        cells = []

        def _fill(x, y, start, new_value):
            if self.grid[x][y] != start or self.grid[x][y] == new_value:
                return
            self.grid[x][y] = new_value
            cells.append((x, y))
            neighbors = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            ]
            for nx, ny in neighbors:
                if 0 <= nx < width and 0 <= ny < height:
                    _fill(nx, ny, start, new_value)

        start_cell = self.grid[start_x][start_y]
        _fill(start_x, start_y, start_cell, new_value)
        return cells


def solve_part1(data: str) -> int:
    grid = Grid(data)
    grid.uniquify_regions()
    return grid.calc_area_and_perimeter()


def solve_part2(data: str) -> int:
    grid = Grid(data)
    grid.uniquify_regions()
    grid.calc_area_and_perimeter()
    return grid.calc_cost_of_sides()


def main():
    data = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 1930, f"Test failed: {part1_test} != 1930"
    print("Part 1 test passed.")

    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 1464678

    part2_test = solve_part2(data)
    assert part2_test == 1206
    part2_result = solve_part2(input_file)
    print(f"Part 2: {part2_result}")
    assert part2_result == 877492


if __name__ == "__main__":
    main()
