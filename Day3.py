import re
import string
import unittest


def unify_symbols(engine_schematic):
    """
    :param engine_schematic: puzzle input; a grid of '.', numbers and other symbols
    :return: returns the puzzle input but with all other symbols replaced with the same symbol x
    """
    symbols = re.escape(string.punctuation.replace('.', ''))
    engine_schematic_simplified = re.sub('['+symbols+']', 'x', engine_schematic)
    return engine_schematic_simplified


def string_to_lines(engine_schematic):
    return engine_schematic.split('\n')


class Grid():
    def __init__(self, grid: list[string]):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
class GridElements:
    def __init__(self, x_coord, y_coord, grid: Grid):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.neighbours = self.identify_neighbours(grid)
        self.adjacent_to_symbol = self.count_adjacent_symbols > 0

    def identify_neighbours(self, grid: Grid):
        neighbours = {}
        check_right_diagonal = False
        check_left_diagonal = False
        if self.x_coord < grid.width:
            neighbours.right = grid[self.y_coord][self.x_coord+1]
            check_right_diagonal = True
        if self.x_coord != 0:
            neighbours.left = grid[self.y_coord][self.x_coord-1]
            check_left_diagonal = True
        if self.y_coord < grid.height:
            neighbours.down = grid[self.y_coord+1][self.x_coord]
            if check_right_diagonal:
                neighbours.down_right = grid[self.y_coord+1][self.x_coord+1]
            if check_left_diagonal:
                neighbours.down_left = grid[self.y_coord+1][self.x_coord-1]
        if self.y_coord != 0:
            neighbours.up = grid[self.y_coord-1][self.x_coord]
            if check_right_diagonal:
                neighbours.up_right = grid[self.y_coord-1][self.x_coord+1]
            if check_left_diagonal:
                neighbours.up_left = grid[self.y_coord-1][self.x_coord-1]
        return neighbours

    def count_adjacent_symbols(self):
        symbols = re.escape(string.punctuation.replace('.', ''))
        n_symbols = len(set(self.neighbours, symbols))
        return n_symbols







def solve_puzzle_part1(engine_schematic):
    simplified_schematic = unify_symbols(engine_schematic)
    simplified_schematic = string_to_lines(simplified_schematic)


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
