import unittest


def find_all_ints(string):
    all_ints = [int(symbol) for symbol in string if symbol.isdigit()]
    return all_ints


def get_first_and_last_int(int_list):
    if len(int_list) == 0:
        return (0, 0)
    elif len(int_list) == 1:
        return int_list[0], int_list[0]
    else:
        return int_list[0], int_list[-1]


def get_calibration_vals(string):
    all_ints = find_all_ints(string)
    relevant_ints = get_first_and_last_int(all_ints)
    calibration_val = str(relevant_ints[0]) + str(relevant_ints[-1])
    return int(calibration_val)

class Test(unittest.TestCase):
    def test_with_provided_input(self):
        provided_data = ("1abc2\n"
                         "pqr3stu8vwx\n"
                         "a1b2c3d4e5f\n"
                         "treb7uchet")
        predicted_answer = [get_calibration_vals(line) for line in provided_data.split("\n")]
        expected_answers = [12, 38, 15, 77]
        self.assertEqual(expected_answers, predicted_answer)


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=3, exit=False)

    with open("inputs/input1.txt") as f:
        data = f.read()
    answer = sum([get_calibration_vals(line) for line in data.split("\n")])
    print(f"Answer: {answer}")
