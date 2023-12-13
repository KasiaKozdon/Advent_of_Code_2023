import unittest

import numpy as np
import numpy.typing as npt


def pattern_to_numpy(pattern):
    n_columns = pattern.index("\n")
    pattern = pattern.replace("\n", "")
    pattern = np.array(list(pattern)).reshape((-1, n_columns))
    return pattern


def vertical_reflexion_column_idx(pattern: npt.NDArray) -> int:
    potential_axes = []
    for column in range(np.shape(pattern)[1]-1):
        if np.array_equal(pattern[:, column], pattern[:, column+1]):
            potential_axes.append(column)
    for column in potential_axes:
        stride = 3
        for col in range(column-1, -1, -1):
            if col + stride > np.shape(pattern)[1]-1:
                break
            if np.array_equal(pattern[:, col], pattern[:, col+stride]):
                stride += 2
            else:
                potential_axes.remove(column)

    potential_axes.append(0)
    return potential_axes[0]


def horizontal_reflexion_column_idx(pattern: npt.NDArray) -> int:
    potential_axes = []
    for row in range(np.shape(pattern)[0]-1):
        if np.array_equal(pattern[row, :], pattern[row+1, :]):
            potential_axes.append(row)
    for row in potential_axes:
        stride = 3
        for r in range(row-1, -1, -1):
            if r + stride > np.shape(pattern)[0]-1:
                break
            if np.array_equal(pattern[r, :], pattern[r+stride, :]):
                stride += 2
            else:
                potential_axes.remove(row)

    potential_axes.append(0)
    return potential_axes[0]


class Test(unittest.TestCase):
    def test_with_provided_inputs(self):
        provided_input_1 = ("#.##..##.\n"
                            "..#.##.#.\n"
                            "##......#\n"
                            "##......#\n"
                            "..#.##.#.\n"
                            "..##..##.\n"
                            "#.#.##.#.")
        provided_input_1_np = pattern_to_numpy(provided_input_1)
        predicted_answer = vertical_reflexion_column_idx(provided_input_1_np) + 1
        expected_answer = 5
        self.assertEqual(expected_answer, predicted_answer)

        provided_input_2 = ("#...##..#\n"
                            "#....#..#\n"
                            "..##..###\n"
                            "#####.##.\n"
                            "#####.##.\n"
                            "..##..###\n"
                            "#....#..#")

        provided_input_2_np = pattern_to_numpy(provided_input_2)
        predicted_answer = horizontal_reflexion_column_idx(provided_input_2_np) + 1
        expected_answer = 4
        self.assertEqual(expected_answer, predicted_answer)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)
