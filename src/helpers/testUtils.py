import random

pt_dn = [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1]
pt_rt = [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1]

mate_pt_dn = {
    0: [1, 3, 5, 6, 7, 8, 10, 12, 14],  # example, replace with actual
    1: [2, 4, 9, 11, 13, 15, 16]
}

mate_pt_rt = {
    0: [1, 2, 3, 5, 7, 9, 12],
    1: [4, 6, 8, 10, 11, 13, 14, 15, 16]
}


def intersect(a, b):
    return [x for x in a if x in b]


def random_choice(arr):
    return random.choice(arr) if arr else 1


def generate_quadrant_pattern(unitCells, seed=None):
    if seed is not None:
        random.seed(seed)

    for i, cell in enumerate(unitCells):
        up_val = 0
        left_val = 0
        if i > 0:
            up_val = unitCells[i-1]["connectedBottom"]
            left_val = unitCells[i-1]["connectedRight"]

        valid_by_up = mate_pt_dn[up_val]
        valid_by_left = mate_pt_rt[left_val]

        valid_patterns = intersect(valid_by_up, valid_by_left)
        cell["patternId"] = random_choice(valid_patterns)

    return unitCells


# Example
unitCells = [
    {"x": 0, "y": 0, "patternId": 0, "connectedRight": False, "connectedBottom": False},
    {"x": 1, "y": 0, "patternId": 0, "connectedRight": False, "connectedBottom": False},
    {"x": 0, "y": 1, "patternId": 0, "connectedRight": False, "connectedBottom": False},
]

pattern = generate_quadrant_pattern(unitCells, seed=42)
for cell in pattern:
    print(cell)
