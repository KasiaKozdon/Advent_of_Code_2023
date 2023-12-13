from itertools import combinations
import re
import unittest


def expand_galaxy(galaxies_map):
    expanded_input = galaxies_map.copy()
    n_added_rows = 0
    n_added_columns = 0
    for idx, row in enumerate(galaxies_map):
        if row == len(row) * row[0]:  # check if all characters are the same
            expanded_input.insert(idx+n_added_rows, row)
            n_added_rows += 1
    for idx, column in enumerate(list(zip(*expanded_input))):
        if column == len(column) * (column[0],):
            expanded_input = [f"{line[:idx+n_added_columns]}.{line[idx+n_added_columns:]}" for line in expanded_input]
            n_added_columns += 1
    return expanded_input


def find_all_galaxies(galaxies_map):
    coords = []
    for idx, line in enumerate(galaxies_map):
        coords.extend([(idx, m.start(0)) for m in re.finditer(pattern="#", string=line)])
    return coords


def find_shortest_distance(paired_galaxy_coords: list[tuple[tuple]]) -> list[int]:
    """
    :param paired_galaxy_coords pairs of coordinates
    :return: minimum distance for each pairs
    """
    distances = [sum(map(lambda i, j: abs(i-j), *pair)) for pair in paired_galaxy_coords]
    return distances


def pair_galaxies(galaxies_coords: list[tuple]):
    pairs = list(combinations(galaxies_coords, 2))
    return pairs


def solve_puzzle_part1(galaxies_map):
    galaxies_map = galaxies_map.strip().split("\n")
    expanded = expand_galaxy(galaxies_map)
    galaxy_coords = find_all_galaxies(expanded)
    galaxy_pairs = pair_galaxies(galaxy_coords)
    return sum(find_shortest_distance(galaxy_pairs))


class Test(unittest.TestCase):
    def test_with_provided_input(self):
        provided_input = ("...#......\n"
                          ".......#..\n"
                          "#.........\n"
                          "..........\n"
                          "......#...\n"
                          ".#........\n"
                          ".........#\n"
                          "..........\n"
                          ".......#..\n"
                          "#...#.....")
        predicted_answer = solve_puzzle_part1(provided_input)
        expected_answer = 374
        self.assertEqual(expected_answer, predicted_answer)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)

    with open("inputs/input11.txt") as f:
        data = f.read().strip()

        answer = solve_puzzle_part1(data)
        print(f"Answer: {answer}")
