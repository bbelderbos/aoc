from collections import deque
from pathlib import Path
from typing import NamedTuple

MAX_PUSHES = 100
COST_BTN_A = 3
COST_BTN_B = 1


class Location(NamedTuple):
    x: int
    y: int


class Button(NamedTuple):
    name: str
    move_to: Location
    cost: int


class Machine(NamedTuple):
    buttons: list[Button]
    prize: Location


def parse_data(data: str) -> list[Machine]:
    blocks = data.split("\n\n")
    machines = []
    for block in blocks:
        lines = block.split("\n")
        buttons = []
        for line in lines:
            parts = line.split(": ")
            name = parts[0]
            move = parts[1].split(", ")
            if name == "Prize":
                x = int(move[0].split("=")[1])
                y = int(move[1].split("=")[1])
                prize = Location(x, y)
            else:
                x = int(move[0].split("+")[1])
                y = int(move[1].split("+")[1])
                cost = COST_BTN_A if name == "Button A" else COST_BTN_B
                buttons.append(Button(name, Location(x, y), cost))
        machines.append(Machine(buttons=buttons, prize=prize))

    return machines


def optimal_button_presses(machine: Machine, max_pushes: int = MAX_PUSHES) -> int:
    queue = deque([(Location(0, 0), [0] * len(machine.buttons), 0)])
    visited = set([(Location(0, 0), tuple([0] * len(machine.buttons)))])

    while queue:
        current_loc, button_pushes, total_cost = queue.popleft()

        if current_loc == machine.prize:
            return total_cost

        for i, button in enumerate(machine.buttons):
            if button_pushes[i] < max_pushes:
                next_loc = Location(
                    current_loc.x + button.move_to.x, current_loc.y + button.move_to.y
                )
                next_pushes = button_pushes[:]
                next_pushes[i] += 1
                next_cost = total_cost + button.cost

                state = (next_loc, tuple(next_pushes))
                if state not in visited:
                    visited.add(state)
                    queue.append((next_loc, next_pushes, next_cost))

    return -1


def solve_part1(data: str) -> int:
    machines = parse_data(data)
    return sum(
        result
        for machine in machines
        if (result := optimal_button_presses(machine)) > 0
    )


# def solve_part2(data: str) -> int:
#     """Solve part 2 of the problem."""


def main():
    data = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".strip()
    input_file = (Path(__file__).parent / "input.txt").read_text().strip()

    part1_test = solve_part1(data)
    assert part1_test == 480
    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 29517

    # part2_test = solve_part2(data)
    # assert part2_test == 0
    # part2_result = solve_part2(input_file)
    # print(f"Part 2: {part2_result}")
    # assert part2_result == 0


if __name__ == "__main__":
    main()
