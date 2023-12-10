import math
import unittest


def generate_race_options(permitted_duration, winning_distance):
    strategy_options = []
    for charging_time in range(permitted_duration):
        race_time = permitted_duration - charging_time
        distance_achieved = race_time * charging_time
        if distance_achieved > winning_distance:
            strategy_options.append(charging_time)
    return strategy_options


def solve_puzzle_part1(race_history: list[dict]):
    strategies_for_all_races = [generate_race_options(**race) for race in race_history]
    count_options = [len(strategy) for strategy in strategies_for_all_races]
    return math.prod(count_options)


class Test(unittest.TestCase):
    def test_with_provided_input(self):
        provided_data = [{"permitted_duration": 7, "winning_distance": 9},
                         {"permitted_duration": 15, "winning_distance": 40},
                         {"permitted_duration": 30, "winning_distance": 200}]

        expected_answer = 288
        predicted_answer = solve_puzzle_part1(provided_data)
        self.assertEqual(expected_answer, predicted_answer)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)

    data = [{"permitted_duration": 42, "winning_distance": 284},
            {"permitted_duration": 68, "winning_distance": 1005},
            {"permitted_duration": 69, "winning_distance": 1122},
            {"permitted_duration": 85, "winning_distance": 1341}]

    answer = solve_puzzle_part1(data)
    print(f"Answer: {answer}")
    