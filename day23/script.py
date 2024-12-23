from collections import defaultdict
from pathlib import Path


def find_triangles(graph, required_character="t"):
    triangles = set()
    for node in graph:
        for neighbor1 in graph[node]:
            for neighbor2 in graph[node]:
                if neighbor1 != neighbor2 and neighbor2 in graph[neighbor1]:
                    triangle = tuple(sorted([node, neighbor1, neighbor2]))
                    if any(t.startswith(required_character) for t in triangle):
                        triangles.add(triangle)
    return triangles


def solve_part1(data: str) -> int:
    graph = defaultdict(set)
    for connection in data.splitlines():
        a, b = connection.split("-")
        graph[a].add(b)
        graph[b].add(a)
    triangles = find_triangles(graph)
    return len(triangles)


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = (Path(__file__).parent / "input_small.txt").read_text().strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 7
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 1108

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
