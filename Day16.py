import unittest

import matplotlib.pyplot as plt
import numpy as np


class Beam:
    def __init__(self, coord_x, coord_y, heading_x, heading_y):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.heading_x = heading_x
        self.heading_y = heading_y

    def step(self):
        self.coord_x += self.heading_x
        self.coord_y += self.heading_y

    def turn_90_degrees_clockwise(self):
        self.heading_x, self.heading_y = -self.heading_y, self.heading_x

    def turn_90_degrees_anticlockwise(self):
        self.heading_x, self.heading_y = self.heading_y, -self.heading_x

    def split_yourself(self):
        """
        Produces another beam, moving in the opposite direction
        :return: beam
        """
        new_beam = Beam(self.coord_x, self.coord_y, -self.heading_x, -self.heading_y)
        new_beam.step()
        return new_beam


def string_to_array(layout_string) -> list[list]:
    layout = layout_string.strip().split("\n")
    layout = [list(line) for line in layout]
    return layout


def tile_in_grid(coord_x, coord_y, grid_width, grid_height):
    y_legal = 0 <= coord_y < grid_height
    x_legal = 0 <= coord_x < grid_width
    return y_legal and x_legal


def get_layout_size(layout):
    layout = string_to_array(layout)
    grid_width = len(layout[0])
    grid_height = len(layout)
    return grid_height, grid_width


def count_visited_tiles(layout, starting_beam):
    layout = string_to_array(layout)
    grid_width = len(layout[0])
    grid_height = len(layout)
    visited_tiles = np.zeros((grid_height, grid_width))
    visited_tiles_history = ""
    beams = [starting_beam]
    for beam in beams:
        while tile_in_grid(beam.coord_x, beam.coord_y, grid_width, grid_height):
            tile = layout[beam.coord_y][beam.coord_x]
            if tile == "\\":
                if beam.heading_x:
                    beam.turn_90_degrees_clockwise()
                else:
                    beam.turn_90_degrees_anticlockwise()
            if tile == "/":
                if beam.heading_x:
                    beam.turn_90_degrees_anticlockwise()
                else:
                    beam.turn_90_degrees_clockwise()
            elif tile == "|":
                if beam.heading_x:
                    beam.turn_90_degrees_clockwise()
                    beams.append(beam.split_yourself())
            elif tile == "-":
                if beam.heading_y:
                    beam.turn_90_degrees_clockwise()
                    beams.append(beam.split_yourself())
            current_position_hash = f";{beam.coord_y},{beam.coord_x},{beam.heading_y},{beam.heading_x};"
            if current_position_hash in visited_tiles_history:
                break  # break tracking beam in a loop
            visited_tiles[beam.coord_y, beam.coord_x] += 1
            visited_tiles_history = visited_tiles_history + current_position_hash
            beam.step()
    plt.imshow(visited_tiles)
    return len(visited_tiles.nonzero()[0])


class Test(unittest.TestCase):
    def test_provided_example(self):
        provided_layout = (".|...\\....\n"
                           "|.-.\\.....\n"
                           ".....|-...\n"
                           "........|.\n"
                           "..........\n"
                           ".........\\\\\n"
                           "..../.\\\\..\n"
                           ".-.-/..|..\n"
                           ".|....-|.\\\n"
                           "..//.|....")
        coord_x = 0
        coord_y = 0
        beam = Beam(coord_x, coord_y, heading_x=1, heading_y=0)
        predicted_answer = count_visited_tiles(provided_layout, beam)
        expected_answer = 46
        self.assertEqual(expected_answer, predicted_answer)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)

    with open("inputs/input16.txt") as f:
        data = f.read()

    # Part 1
    coord_x = 0
    coord_y = 0
    beam = Beam(coord_x, coord_y, heading_x=1, heading_y=0)
    answer = count_visited_tiles(data, beam)
    print(f"Answer to part 1: {answer}")

    # Part 2
    possible_answers = []
    height, width = get_layout_size(data)

    # left edge
    coord_x, heading_x, heading_y = 0, 1, 0
    for coord_y in range(0, height):
        beam = Beam(coord_x, coord_y, heading_x, heading_y)
        possible_answers.append(count_visited_tiles(data, beam))
    # right edge
    coord_x, heading_x, heading_y = width-1, -1, 0
    for coord_y in range(0, height):
        beam = Beam(coord_x, coord_y, heading_x, heading_y)
        possible_answers.append(count_visited_tiles(data, beam))
    # top edge
    coord_y, heading_x, heading_y = 0, 0, 1
    for coord_x in range(0, width):
        beam = Beam(coord_x, coord_y, heading_x, heading_y)
        possible_answers.append(count_visited_tiles(data, beam))
    # bottom edge
    coord_y, heading_x, heading_y = height-1, 0, -1
    for coord_x in range(0, width):
        beam = Beam(coord_x, coord_y, heading_x, heading_y)
        possible_answers.append(count_visited_tiles(data, beam))

    print(f"Answer to part 2: {max(possible_answers)}")
