import math
import re
import unittest


def find_numbers_before_keyword(string, keyword):
    """
    :param string:
    :param keyword:
    :return: list of ints before each instance of the keyword. If no found, returns one 0
    """
    numbers = re.findall(f"([0-9]+) {keyword}", string)
    numbers = [int(entry) for entry in numbers]
    return numbers if len(numbers) > 0 else [0]


def parse_games_info(games_info):
    """
    :param games_info:
    :return: dictionary of dictionaries game_id: {reds: [int], greens: [int], blues: [int]}
    """
    games_info_lines = games_info.split("\n")
    parsed_game_info = {}
    for game in games_info_lines:
        game_id = re.findall(r"Game ([0-9]+):", game)[0]
        game_id = int(game_id)
        reds = find_numbers_before_keyword(string=game, keyword="red")
        greens = find_numbers_before_keyword(string=game, keyword="green")
        blues = find_numbers_before_keyword(string=game, keyword="blue")
        parsed_game_info[game_id] = {"reds": reds, "greens": greens, "blues": blues}
    return parsed_game_info


def check_if_true(observations: dict, assumption: dict):
    for category in observations.keys():
        count_of_impossible = [1 for obs in observations[category] if obs > assumption[category]]
        if len(count_of_impossible) > 0:
            return False
    return True


def find_ids_of_possible_games(games_info, query):
    extracted_stats = parse_games_info(games_info)
    possible_games = []
    for game_id, stats in extracted_stats.items():
        if check_if_true(observations=stats, assumption=query):
            possible_games.append(game_id)
    return possible_games


def find_minimum_resource_required(game: dict):
    minimum_required = {}
    for category, values in game.items():
        minimum_required[category] = max(values)
    return minimum_required


def apply_required_transform(minimum_sets: list):
    products = [math.prod(ms.values()) for ms in minimum_sets]
    return sum(products)


def solve_puzzle_part1(games_info, query):
    return sum(find_ids_of_possible_games(games_info, query))


def solve_puzzle_part2(games_info):
    extracted_stats = parse_games_info(games_info)
    resources_required = []
    for game_id, stats in extracted_stats.items():
        resources_required.append(find_minimum_resource_required(stats))
    puzzle2_answer = apply_required_transform(resources_required)
    return puzzle2_answer


class Test(unittest.TestCase):
    def test_with_provided_input(self):
        provided_data = ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n"
                         "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n"
                         "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n"
                         "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n"
                         "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")

        query = {"reds": 12, "greens": 13, "blues": 14}
        expected_answer = sum([1, 2, 5])  # game IDs
        predicted_answer = solve_puzzle_part1(provided_data, query)
        self.assertEqual(expected_answer, predicted_answer)

    def test_with_provided_input_part2(self):
        provided_data = ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n"
                         "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n"
                         "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n"
                         "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n"
                         "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")

        expected_answer = sum([48, 12, 1560, 630, 36])
        predicted_answer = solve_puzzle_part2(provided_data)
        self.assertEqual(expected_answer, predicted_answer)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)

    with open("inputs/input2.txt") as f:
        data = f.read()
    data = data.strip()
    data_query = {"reds": 12, "greens": 13, "blues": 14}

    # Part 1
    answer = solve_puzzle_part1(data, data_query)
    print(f"Answer: {answer}")

    # Part 2
    answer = solve_puzzle_part2(data)
    print(f"Answer: {answer}")
