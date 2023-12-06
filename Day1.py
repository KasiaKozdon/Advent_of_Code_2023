import re
import unittest


def find_all_ints(string):
    """
    :param string: any string which may contain integers
    :return: dictionary {index: number value}
    """
    found_ints = {idx: int(symbol) for idx, symbol in enumerate(string) if symbol.isdigit()}
    return found_ints


def find_all_number_strings(string):
    """
        :param string: any string which may contain number substrings
        :return: dictionary {index: number value}
    """
    possible_numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    found_numbers = {}
    for number in possible_numbers:
        if number in string:
            number_value = number_name_to_int(number)
            sub_dict = {instance.start(): number_value for instance in re.finditer(number, string)}
            found_numbers.update(sub_dict)
    return found_numbers


def get_first_and_last_int(integers: dict):
    keys_list = list(integers.keys())
    if len(integers) == 0:
        return 0, 0
    else:
        return integers[min(keys_list)], integers[max(keys_list)]


def concatenate_ints(integers: list) -> int:
    number_string = str(integers[0]) + str(integers[-1])
    return int(number_string)


def number_name_to_int(num_string):
    numbers_dict = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                    "six": 6, "seven": 7, "eight": 8, "nine": 9}
    return numbers_dict[num_string]


def get_calibration_vals(string, include_strings=False):
    all_numbers = find_all_ints(string)
    if include_strings:
        all_numbers.update(find_all_number_strings(string))
    relevant_ints = get_first_and_last_int(all_numbers)
    return concatenate_ints(relevant_ints)

class Test(unittest.TestCase):
    def test_with_provided_input(self):
        provided_data = ("1abc2\n"
                         "pqr3stu8vwx\n"
                         "a1b2c3d4e5f\n"
                         "treb7uchet")
        predicted_answer = [get_calibration_vals(line) for line in provided_data.split("\n")]
        expected_answers = [12, 38, 15, 77]
        self.assertEqual(expected_answers, predicted_answer)

    def test_with_provided_input_part2(self):
        provided_data = ("two1nine\n"
                         "eightwothree\n"
                         "abcone2threexyz\n"
                         "xtwone3four\n"
                         "4nineeightseven2\n"
                         "zoneight234\n"
                         "7pqrstsixteen")

        predicted_answer = [get_calibration_vals(line, include_strings=True) for line in provided_data.split("\n")]
        expected_answers = [29, 83, 13, 24, 42, 14, 76]
        self.assertEqual(expected_answers, predicted_answer)


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=3, exit=False)

    with open("inputs/input1.txt") as f:
        data = f.read()
    # Part 1
    answer = sum([get_calibration_vals(line) for line in data.split("\n")])
    print(f"Answer: {answer}")

    # Part 2
    answer = sum([get_calibration_vals(line, include_strings=True) for line in data.split("\n")])
    print(f"Answer: {answer}")
