import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import wraps
from heapq import heappop, heappush
from pathlib import Path
from typing import NamedTuple

MAX_PUSHES = 100
COST_BTN_A = 3
COST_BTN_B = 1


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.pop("timeit", True):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            print(f"{func.__name__} took {time.perf_counter() - start:.6f} seconds")
            return result
        else:
            return func(*args, **kwargs)

    return wrapper


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


def parse_data(data: str, add_to_price=0) -> list[Machine]:
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
                prize = Location(x + add_to_price, y + add_to_price)
            else:
                x = int(move[0].split("+")[1])
                y = int(move[1].split("+")[1])
                cost = COST_BTN_A if name == "Button A" else COST_BTN_B
                buttons.append(Button(name, Location(x, y), cost))
        machines.append(Machine(buttons=buttons, prize=prize))

    return machines


def optimal_button_presses(machine: Machine, max_pushes: int = MAX_PUSHES) -> int:
    queue = []
    heappush(queue, (0, Location(0, 0), [0] * len(machine.buttons)))
    visited = set([(Location(0, 0), 0)])

    while queue:
        total_cost, current_loc, button_pushes = heappop(queue)

        if current_loc == machine.prize:
            return total_cost

        for i, button in enumerate(machine.buttons):
            if button_pushes[i] < max_pushes:
                next_loc = Location(
                    current_loc.x + button.move_to.x, current_loc.y + button.move_to.y
                )

                # skip if the next location is out of bounds
                if next_loc.x > machine.prize.x or next_loc.y > machine.prize.y:
                    continue

                next_pushes = button_pushes[:]
                next_pushes[i] += 1
                next_cost = total_cost + button.cost

                state = (next_loc, next_cost)
                if state not in visited:
                    visited.add(state)
                    heappush(queue, (next_cost, next_loc, next_pushes))

    return -1


@timeit
def solve_part1(data: str, timeit=True) -> int:
    machines = parse_data(data)
    return sum(
        result
        for machine in machines
        if (result := optimal_button_presses(machine)) > 0
    )


@timeit
def solve_part1_parallel(data: str, timeit=True) -> int:
    machines = parse_data(data)

    with ProcessPoolExecutor() as executor:
        results = executor.map(optimal_button_presses, machines)

    return sum(result for result in results if result > 0)


@timeit
def solve_part1_threaded(data: str, timeit=True) -> int:
    machines = parse_data(data)

    with ThreadPoolExecutor() as executor:
        results = executor.map(optimal_button_presses, machines)

    return sum(result for result in results if result > 0)


def optimal_button_cost(button_a, button_b, prize):
    ax, ay = button_a.move_to.x, button_a.move_to.y
    bx, by = button_b.move_to.x, button_b.move_to.y
    px, py = prize.x, prize.y

    # Solve for b (Button B presses) using elimination
    b_presses = (px * ay - py * ax) // (ay * bx - by * ax)
    # Solve for a (Button A presses) using the result of b
    a_presses = (px * by - py * bx) // (by * ax - bx * ay)

    # Validate the solution
    if ax * a_presses + bx * b_presses == px and ay * a_presses + by * b_presses == py:
        total_cost = 3 * a_presses + b_presses
        return a_presses, b_presses, total_cost
    else:
        return None, None, None


def solve_part2(data: str) -> int:
    """Solve part 2 of the problem."""
    machines = parse_data(data, add_to_price=10000000000000)
    total_cost = 0

    for machine in machines:
        button_a, button_b = machine.buttons
        a, b, cost = optimal_button_cost(button_a, button_b, machine.prize)

        if cost is not None:
            total_cost += cost

    return total_cost


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

    part1_test = solve_part1(data, timeit=False)
    assert part1_test == 480

    part1_result = solve_part1(input_file)
    print(f"Part 1: {part1_result}")
    assert part1_result == 29517

    part1_result = solve_part1_threaded(input_file)
    print(f"Part 1 (threaded): {part1_result}")
    assert part1_result == 29517

    part1_result = solve_part1_parallel(input_file)
    print(f"Part 1 (parallel): {part1_result}")
    assert part1_result == 29517

    part2_test = solve_part2(data)
    assert part2_test == 875318608908
    part2_result = solve_part2(input_file)
    print(f"Part 2: {part2_result}")
    assert part2_result == 103570327981381


if __name__ == "__main__":
    main()
