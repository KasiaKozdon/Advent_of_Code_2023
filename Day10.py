import unittest
import matplotlib.pyplot as plt
import numpy as np


def string_to_numpy(puzzle_input: str):
    row_len = puzzle_input.index("\n")
    symbols = [*(puzzle_input.replace("\n", ""))]
    return np.asarray(symbols).reshape((row_len, -1))


def find_start_coords(grid):
    return tuple(zip(*np.where(grid == "S")))[0]


def find_next_coords(grid, all_previous_coords):
    def check_above():
        if y > 0:  # check above
            if grid[(coords := (y-1, x))] in ["|", "7", "F", "S"]:
                connection_coords.append((coords))

    def check_below():
        if y < grid_height:  # check below
            if grid[(coords := (y+1, x))] in ["|", "L", "J", "S"]:
                connection_coords.append((coords))

    def check_left():
        if x > 0:  # check left
            if grid[(coords := (y, x-1))] in ["-", "L", "F", "S"]:
                connection_coords.append((coords))

    def check_right():
        if x < grid_width:  # check right
            if grid[(coords := (y, x+1))] in ["-", "J", "7", "S"]:
                connection_coords.append((coords))

    current_coords = all_previous_coords[-1]
    symbol = grid[(y := current_coords[0]), (x := current_coords[1])]
    grid_width, grid_height = np.shape(grid)

    # Each symbol can connect with limited set of neighbouring directions
    connection_coords = []
    if symbol == "|":
        check_above()
        check_below()
    elif symbol == "-":
        check_left()
        check_right()
    elif symbol == "L":
        check_right()
        check_above()
    elif symbol == "J":
        check_left()
        check_above()
    elif symbol == "7":
        check_left()
        check_below()
    elif symbol == "F":
        check_right()
        check_below()
    elif symbol == "S":
        check_left()
        check_right()
        check_above()
        check_below()
    if len(all_previous_coords) > 1:
        connection_coords.remove(all_previous_coords[-2])  # avoid loop - remove step that go you to the current position
    return connection_coords[0]

def traverse_grid(grid):
    start_coords = find_start_coords(grid)
    current_coords = start_coords
    path_taken = []
    while True:
        path_taken.append(current_coords)
        current_coords = find_next_coords(grid, path_taken)
        if start_coords == current_coords:
            break
    return path_taken


def solve_puzzle_part1(puzzle_input):
    piping_grid = string_to_numpy(puzzle_input)
    journey = traverse_grid(piping_grid)
    return len(journey)//2


def solve_puzzle_part2(puzzle_input):
    piping_grid = string_to_numpy(puzzle_input)
    journey = traverse_grid(piping_grid)
    y = np.asarray(journey)[:, 0]
    x = np.asarray(journey)[:, 1]
    plt.plot(x, y)
    return None


class Test(unittest.TestCase):
    def test_with_provided_input(self):
        provided_data = (".....\n"
                        ".S-7.\n"
                        ".|.|.\n"
                        ".L-J.\n"
                        ".....")
        predicted_answer = solve_puzzle_part1(provided_data)
        expected_answer = 4
        self.assertEqual(expected_answer, predicted_answer)

        provided_data = ("..F7.\n"
                         ".FJ|.\n"
                         "SJ.L7\n"
                         "|F--J\n"
                         "LJ...")
        predicted_answer = solve_puzzle_part1(provided_data)
        expected_answer = 8
        self.assertEqual(expected_answer, predicted_answer)


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=3, exit=False)

    with open("inputs/input10.txt") as f:
        data = f.read().strip()

    answer = solve_puzzle_part1(data)
    print(f"Answer: {answer}")

    answer = solve_puzzle_part2(data)
    print(f"Answer: {answer}")