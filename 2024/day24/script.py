from pathlib import Path


def _operation(op: str, wire1: int, wire2: int) -> int:
    match op:
        case "AND":
            return wire1 & wire2
        case "OR":
            return wire1 | wire2
        case "XOR":
            return wire1 ^ wire2
        case _:
            raise ValueError(f"Invalid operation: {op}")


def solve_part1(data: str) -> int:
    """Solve part 1 of the problem."""
    wires_str, ops_str = data.split("\n\n")
    wires = {}
    pending_ops = []

    for wire in wires_str.splitlines():
        key, value = wire.split(": ")
        wires[key] = int(value)

    for operation in ops_str.splitlines():
        pending_ops.append(operation)

    # make sure we process in the right order
    while pending_ops:
        remaining_ops = []
        for operation in pending_ops:
            parts, res = operation.split(" -> ")
            wire1, op, wire2 = parts.split(" ")
            if wire1 in wires and wire2 in wires:
                wires[res] = _operation(op, wires[wire1], wires[wire2])
            else:
                remaining_ops.append(operation)
        if len(remaining_ops) == len(pending_ops):
            raise ValueError("Circular dependency or unresolved wires!")
        pending_ops = remaining_ops

    zz = {k: v for k, v in wires.items() if k.startswith("z")}
    z_bin = "".join([str(v) for k, v in sorted(zz.items(), reverse=True)])

    return int(z_bin, 2)


def main():
    data = (Path(__file__).parent / "input_small.txt").read_text().strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 2024
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 69201640933606


if __name__ == "__main__":
    main()
