from collections import defaultdict
from pathlib import Path


def find_triangles(
    graph: dict[str, set[str]], required_character: str = "t"
) -> set[tuple[str, ...]]:
    triangles = set()
    for node in graph:
        for neighbor1 in graph[node]:
            for neighbor2 in graph[node]:
                if neighbor1 != neighbor2 and neighbor2 in graph[neighbor1]:
                    triangle = tuple(sorted([node, neighbor1, neighbor2]))
                    if any(t.startswith(required_character) for t in triangle):
                        triangles.add(triangle)
    return triangles


def build_graph(data: str) -> dict[str, set[str]]:
    graph = defaultdict(set)
    for connection in data.splitlines():
        a, b = connection.split("-")
        graph[a].add(b)
        graph[b].add(a)
    return graph


def solve_part1(data: str) -> int:
    graph = build_graph(data)
    triangles = find_triangles(graph)
    return len(triangles)


def bron_kerbosch(graph, r=None, p=None, x=None, cliques=None):
    r = r if r is not None else set()
    p = p if p is not None else set(graph.keys())
    x = x if x is not None else set()
    cliques = cliques if cliques is not None else []

    if not p and not x:
        cliques.append(r)
        return

    for node in list(p):
        bron_kerbosch(graph, r | {node}, p & graph[node], x & graph[node], cliques)
        p.remove(node)
        x.add(node)
    return cliques


def find_largest_clique(graph: dict[str, set[str]]) -> list[str]:
    cliques = bron_kerbosch(graph)
    largest_clique = max(cliques, key=len)
    return sorted(largest_clique)


def solve_part2(data: str) -> str:
    graph = build_graph(data)
    return ",".join(find_largest_clique(graph))


def main():
    data = (Path(__file__).parent / "input_small.txt").read_text().strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 7
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 1108

    data = (Path(__file__).parent / "input_small2.txt").read_text().strip()
    part2_test = solve_part2(data)
    assert part2_test == "co,de,ka,ta"
    part2_result = solve_part2(input_file)
    print(f"Part 2: {part2_result}")
    assert part2_result == "ab,cp,ep,fj,fl,ij,in,ng,pl,qr,rx,va,vf"


if __name__ == "__main__":
    main()
