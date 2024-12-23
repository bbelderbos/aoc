from pathlib import Path


def combo(registers: dict[str, int], o: int) -> int:
    match o:
        case 0 | 1 | 2 | 3:
            return o
        case 4:
            return registers["A"]
        case 5:
            return registers["B"]
        case 6:
            return registers["C"]
        case 7:
            raise ValueError("Operand 7 is reserved and cannot be used.")
        case _:
            raise ValueError(f"Invalid operation: {o}")


def solve_part1(data: str) -> int:
    registers_str, program_str = data.split("\n\n")
    registers = {
        line.split(": ")[0].replace("Register ", ""): int(line.split(": ")[1])
        for line in registers_str.splitlines()
    }

    ops = [int(step) for step in program_str.split(": ")[1].split(",")]

    pointer = 0
    results = []

    while True:
        pointer_changed_in_loop = False
        try:
            opcode = ops[pointer]
            operand = ops[pointer + 1]
        except IndexError:
            break

        match opcode:
            case 0:
                registers["A"] = registers["A"] // 2 ** combo(registers, operand)
            case 1:
                registers["B"] ^= operand
            case 2:
                registers["B"] = combo(registers, operand) % 8
            case 3:
                if registers["A"] != 0:
                    pointer = operand
                    pointer_changed_in_loop = True
            case 4:
                registers["B"] ^= registers["C"]
            case 5:
                results.append(combo(registers, operand) % 8)
            case 6:
                registers["B"] = registers["A"] // 2 ** combo(registers, operand)
            case 7:
                registers["C"] = registers["A"] // 2 ** combo(registers, operand)
            case _:
                raise ValueError(f"Invalid operation: {opcode}")

        if not pointer_changed_in_loop:
            pointer += 2

    return ",".join(map(str, results))


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""".strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert (
        part1_test == "4,6,3,5,6,3,5,2,1,0"
    ), f"Expected 4,6,3,5,6,3,5,2,1,0 but got {part1_test}"
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == "7,4,2,0,5,0,5,3,7"

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
