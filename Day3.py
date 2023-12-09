import re
import string
import unittest

import numpy as np


def string_to_lines(grid_description):
    return grid_description.split('\n')


def unify_symbols(engine_schematic):
    """
    :param engine_schematic: puzzle input; a grid of '.', numbers and other symbols
    :return: returns the puzzle input but with all other symbols replaced with the same symbol x
    """
    symbols = re.escape(string.punctuation.replace('.', ''))
    engine_schematic_simplified = re.sub('[' + symbols + ']', 'x', engine_schematic)
    return engine_schematic_simplified


class Grid:
    def __init__(self, grid_description: string):
        self.grid = unify_symbols(grid_description)
        self.grid = string_to_lines(self.grid)
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.grid_elements = self.initialise_grid_elements()

    def initialise_grid_elements(self):
        grid_elements = []
        for r_idx, row in enumerate(self.grid):
            temp = []
            for s_idx, symbol in enumerate(row):
                temp.append(GridElement(y_coord=r_idx, x_coord=s_idx, grid=self))
            grid_elements.append(temp)
        return grid_elements

    def make_survival_mask(self):
        survival_mask = np.zeros((self.height, self.width))
        for r_idx, row in enumerate(self.grid_elements):
            for s_idx, entry in enumerate(row):
                survival_mask[r_idx, s_idx] = self.grid_elements[r_idx][s_idx].survives
        return survival_mask

    def apply_survival_mask(self, survival_mask):
        for r_idx, row in enumerate(self.grid):
            for s_idx, entry in enumerate(row):
                if not survival_mask[r_idx, s_idx]:
                    self.grid[r_idx] = ''.join([self.grid[r_idx][:s_idx], "d", self.grid[r_idx][s_idx+1:]])

    def grid_to_string(self):
        partial = [''.join(row) for row in self.grid]
        return ' '.join(partial)


class GridElement:
    def __init__(self, y_coord, x_coord, grid: Grid):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.neighbours = self.identify_neighbours(grid)
        self.survives = grid.grid[y_coord][x_coord].isdigit() and self.count_adjacent_symbols() > 0
        self.offers_survival = self.survives or grid.grid[y_coord][x_coord] == "x"

    def identify_neighbours(self, grid: Grid):
        neighbours = {}
        check_right_diagonal = False
        check_left_diagonal = False
        if self.x_coord < grid.width - 1:
            neighbours["right"] = grid.grid[self.y_coord][self.x_coord+1]
            check_right_diagonal = True
        if self.x_coord != 0:
            neighbours["left"] = grid.grid[self.y_coord][self.x_coord-1]
            check_left_diagonal = True
        if self.y_coord < grid.height - 1:
            neighbours["down"] = grid.grid[self.y_coord+1][self.x_coord]
            if check_right_diagonal:
                neighbours["down_right"] = grid.grid[self.y_coord+1][self.x_coord+1]
            if check_left_diagonal:
                neighbours["down_left"] = grid.grid[self.y_coord+1][self.x_coord-1]
        if self.y_coord != 0:
            neighbours["up"] = grid.grid[self.y_coord-1][self.x_coord]
            if check_right_diagonal:
                neighbours["up_right"] = grid.grid[self.y_coord-1][self.x_coord+1]
            if check_left_diagonal:
                neighbours["up_left"] = grid.grid[self.y_coord-1][self.x_coord-1]
        return neighbours

    def count_adjacent_symbols(self):
        symbols = "x"  # re.escape(string.punctuation.replace('.', ''))
        n_symbols = len([i for i in self.neighbours.values() if i in symbols])
        return n_symbols

    def update_survival(self, grid: Grid):
        if self.survives:
            return
        # Check left neighbour
        if grid.grid[self.y_coord][self.x_coord].isdigit():
            if self.x_coord != 0:
                if grid.grid_elements[self.y_coord][self.x_coord-1].offers_survival:
                    self.survives = True
                    self.offers_survival = True
                    return
        # Check right neighbour
            if self.x_coord < grid.width - 1:
                if grid.grid_elements[self.y_coord][self.x_coord+1].offers_survival:
                    self.survives = True
                    self.offers_survival = True
                    return


def solve_puzzle_part1(engine_schematic):
    extracted_info = Grid(engine_schematic)
    n_updates_required_worst_case = extracted_info.width
    updates = 0
    while updates != n_updates_required_worst_case:
        [entry.update_survival(extracted_info) for row in extracted_info.grid_elements for entry in row]
        updates += 1
    survival_mask = extracted_info.make_survival_mask()
    extracted_info.apply_survival_mask(survival_mask)
    numbers = re.findall(f"[0-9]+", extracted_info.grid_to_string())
    return sum([int(nr) for nr in numbers])


class Test(unittest.TestCase):
    def test_with_provided_input(self):
        provided_data = ("467..114..\n"
                         "...*......\n"
                         "..35..633.\n"
                         "......#...\n"
                         "617*......\n"
                         ".....+.58.\n"
                         "..592.....\n"
                         "......755.\n"
                         "...$.*....\n"
                         ".664.598..")

        expected_answer = 4361
        predicted_answer = solve_puzzle_part1(provided_data)
        self.assertEqual(expected_answer, predicted_answer)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)

    with open("inputs/input3.txt") as f:
        data = f.read().strip()
    answer = solve_puzzle_part1(data)
    print(f"Answer: {answer}")
