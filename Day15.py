import re
import unittest


def hash_string(to_hash: str) -> int:
    hash_value = 0
    for character in to_hash:
        hash_value = ((hash_value + ord(character)) * 17) % 256
    return hash_value


def calculate_lenses_power(instructions: str) -> int:
    lens_names = re.findall(r'[a-z]+', instructions)
    boxes_ids = [hash_string(name) for name in lens_names]
    boxes_content = {box_id: {} for box_id in boxes_ids}
    operations = re.findall(r'[=-]+', instructions)
    focal_lengths = re.findall(r"[0-9]+", instructions)
    focal_lengths = [int(fl) for fl in focal_lengths]

    for idx, operation in enumerate(operations):
        box_id = boxes_ids[idx]
        if operation == "-":
            if (lens_to_remove := lens_names[idx]) in boxes_content[box_id].keys():
                boxes_content[box_id].pop(lens_to_remove)
        elif operation == "=":
            content_value = focal_lengths.pop(0)
            boxes_content[box_id][lens_names[idx]] = content_value

    lens_powers = []
    for idx, contents in boxes_content.items():
        for lens_idx, lens in enumerate(contents.items()):
            lens_powers.append((1 + idx) * (lens_idx + 1) * lens[1])

    return sum(lens_powers)


class Test(unittest.TestCase):
    def test_with_provided_example_hash(self):
        provided_input = "HASH"
        predicted_answer = hash_string(provided_input)
        expected_answer = 52
        self.assertEqual(expected_answer, predicted_answer)

    def test_with_provided_example_part1(self):
        provided_input = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(",")
        predicted_answer = sum([hash_string(command) for command in provided_input])
        expected_answer = 1320
        self.assertEqual(expected_answer, predicted_answer)

    def test_with_provided_example_part2(self):
        provided_input = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
        predicted_answer = calculate_lenses_power(provided_input)
        expected_answer = 145
        self.assertEqual(expected_answer, predicted_answer)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)

    with open("inputs/input15.txt") as f:
        data = f.read().strip()

    answer = sum([hash_string(command) for command in data])
    print(f"Answer to part 1: {answer}")

    answer = calculate_lenses_power(data)
    print(f"Answer to part 2: {answer}")
