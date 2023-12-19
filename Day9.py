import re
import unittest

import numpy as np


def find_next_number_part1(puzzle):
    differences = puzzle.copy()
    rightmost = []
    while True:
        rightmost.insert(0, differences[-1])
        differences = np.diff(differences)
        if not np.any(differences):
            break
    return sum(rightmost)


def find_next_number_part2(puzzle):
    differences = puzzle.copy()
    leftmost = []
    while True:
        leftmost.insert(0, differences[0])
        differences = np.diff(differences)
        if not np.any(differences):
            leftmost.insert(0, differences[0])
            break
    sequence_start = 0
    for i in range(0, len(leftmost)):
        sequence_start = leftmost[i] - sequence_start
    return sequence_start


def solve_puzzles(raw_puzzle_input, search_funct=find_next_number_part1):
    individual_puzzles = raw_puzzle_input.split("\n")
    individual_puzzles = [re.findall(r"-?[0-9]+", puzzle) for puzzle in individual_puzzles]
    individual_puzzles = [np.array(puzzle, dtype=int) for puzzle in individual_puzzles]
    partial_solutions = [search_funct(puzzle) for puzzle in individual_puzzles]
    return sum(partial_solutions)


class Test(unittest.TestCase):
    def test_with_provided_example(self):
        provided_data = ("0 3 6 9 12 15\n"
                         "1 3 6 10 15 21\n"
                         "10 13 16 21 30 45")
        # partial_answer_row0, partial_answer_row1, partial_answer_row2 = 18, 28, 68
        expected_answer = 114
        predicted_answer = solve_puzzles(provided_data)
        self.assertEqual(expected_answer, predicted_answer)

        expected_answer = 2
        predicted_answer = solve_puzzles(provided_data, find_next_number_part2)
        self.assertEqual(expected_answer, predicted_answer)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)

    with open("inputs/input9.txt") as f:
        data = f.read().strip()

    answer = solve_puzzles(data)
    print(f"Answer part 1: {answer}")

    answer = solve_puzzles(data, find_next_number_part2)
    print(f"Answer part 1: {answer}")