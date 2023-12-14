import unittest

import numpy as np
import numpy.typing as npt


# TODO: optimise

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
    correct_axes = potential_axes.copy()
    for column in potential_axes:
        for col in range(0, column):
            stride = (column - col) * 2 + 1
            if col + stride < np.shape(pattern)[1]:
                if not np.array_equal(pattern[:, col], pattern[:, col+stride]):
                    correct_axes.remove(column)
                    break

    if len(correct_axes) > 0:
        return correct_axes[0] + 1
    else:
        return 0


def smudged_vertical_reflexion_column_idx(pattern: npt.NDArray) -> int:
    potential_axes = []
    smudge_tracking = []
    for column in range(np.shape(pattern)[1]-1):
        if (smudge := sum(pattern[:, column] != pattern[:, column+1])) <= 1:
            potential_axes.append(column)
            smudge_tracking.append(smudge)
    correct_axes = potential_axes.copy()
    for idx, column in enumerate(potential_axes):
        for col in range(0, column):
            stride = (column - col) * 2 + 1
            if col + stride < np.shape(pattern)[1]:
                if (smudge := sum(pattern[:, col] != pattern[:, col+stride])):
                    smudge_tracking[idx] += smudge
                    if smudge_tracking[idx] > 1:
                        correct_axes.remove(column)
                        break

    for idx, pa in enumerate(potential_axes):
        if smudge_tracking[idx] == 0:
            correct_axes.remove(pa)
    if len(correct_axes) > 0:
        return correct_axes[0] + 1
    else:
        return 0


def smudged_horizontal_reflexion_column_idx(pattern: npt.NDArray) -> int:
    potential_axes = []
    smudge_tracking = []
    for row in range(np.shape(pattern)[0]-1):
        if (smudge := sum(pattern[row, :] != pattern[row+1, :])) <= 1:
            potential_axes.append(row)
            smudge_tracking.append(smudge)
    correct_axes = potential_axes.copy()
    for idx, row in enumerate(potential_axes):
        for r in range(0, row):
            stride = (row - r) * 2 + 1
            if r + stride < np.shape(pattern)[0]:
                if (smudge := sum(pattern[r, :] != pattern[r+stride, :])):
                    smudge_tracking[idx] += smudge
                    if smudge_tracking[idx] > 1:
                        correct_axes.remove(row)
                        break

    for idx, pa in enumerate(potential_axes):
        if smudge_tracking[idx] == 0:
            correct_axes.remove(pa)
    if len(correct_axes) > 0:
        return correct_axes[0] + 1
    else:
        return 0


def horizontal_reflexion_column_idx(pattern: npt.NDArray) -> int:
    potential_axes = []
    for row in range(np.shape(pattern)[0]-1):
        if np.array_equal(pattern[row, :], pattern[row+1, :]):
            potential_axes.append(row)
    correct_axes = potential_axes.copy()
    for row in potential_axes:
        for r in range(0, row):
            stride = (row - r) * 2 + 1
            if r + stride < np.shape(pattern)[0]:
                if not np.array_equal(pattern[r, :], pattern[r+stride, :]):
                    correct_axes.remove(row)
                    break

    if len(correct_axes) > 0:
        return correct_axes[0] + 1
    else:
        return 0


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
        predicted_answer = vertical_reflexion_column_idx(provided_input_1_np)
        expected_answer = 5
        self.assertEqual(expected_answer, predicted_answer)

        predicted_answer = horizontal_reflexion_column_idx(provided_input_1_np)
        expected_answer = 0
        self.assertEqual(expected_answer, predicted_answer)

        provided_input_2 = ("#...##..#\n"
                            "#....#..#\n"
                            "..##..###\n"
                            "#####.##.\n"
                            "#####.##.\n"
                            "..##..###\n"
                            "#....#..#")

        provided_input_2_np = pattern_to_numpy(provided_input_2)
        predicted_answer = horizontal_reflexion_column_idx(provided_input_2_np)
        expected_answer = 4
        self.assertEqual(expected_answer, predicted_answer)

        predicted_answer = vertical_reflexion_column_idx(provided_input_2_np)
        expected_answer = 0
        self.assertEqual(expected_answer, predicted_answer)

    def test_edge_counts(self):
        provided_input_1 = ("..##..##.\n"
                            "..#.##.#.\n"
                            "..#.##.#.")
        provided_input_1_np = pattern_to_numpy(provided_input_1)
        predicted_answer = vertical_reflexion_column_idx(provided_input_1_np)
        expected_answer = 1
        self.assertEqual(expected_answer, predicted_answer)

        provided_input_1 = ("#.##..#..\n"
                            "..#.##...\n"
                            "#.#.##...")
        provided_input_1_np = pattern_to_numpy(provided_input_1)
        predicted_answer = vertical_reflexion_column_idx(provided_input_1_np)
        expected_answer = 8
        self.assertEqual(expected_answer, predicted_answer)

        provided_input_2 = ("#####.##.\n"
                            "#####.##.\n"
                            "..##..###\n"
                            "#....#..#")

        provided_input_2_np = pattern_to_numpy(provided_input_2)
        predicted_answer = horizontal_reflexion_column_idx(provided_input_2_np)
        expected_answer = 1
        self.assertEqual(expected_answer, predicted_answer)

        provided_input_2 = ("#...##..#\n"
                            "#....#..#\n"
                            "..##..###\n"
                            "#####.##.\n"
                            "#####.##.")

        provided_input_2_np = pattern_to_numpy(provided_input_2)
        predicted_answer = horizontal_reflexion_column_idx(provided_input_2_np)
        expected_answer = 4
        self.assertEqual(expected_answer, predicted_answer)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)

    with open("inputs/input13.txt") as f:
        data = f.read()

    vertical_reflections = []
    horizontal_reflections = []
    data = data.split("\n\n")
    for datum in data:
        datum = pattern_to_numpy(datum)
        vertical_reflections.append(vertical_reflexion_column_idx(datum))
        horizontal_reflections.append(horizontal_reflexion_column_idx(datum))
    answer = sum(vertical_reflections) + sum([h * 100 for h in horizontal_reflections])
    print(f"Answer: {answer}")


    # Part 2
    vertical_reflections = []
    horizontal_reflections = []
    for datum in data:
        datum = pattern_to_numpy(datum)
        vertical_reflections.append(smudged_vertical_reflexion_column_idx(datum))
        horizontal_reflections.append(smudged_horizontal_reflexion_column_idx(datum))
    answer = sum(vertical_reflections) + sum([h * 100 for h in horizontal_reflections])
    print(f"Answer: {answer}")
