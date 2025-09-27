import random
import math
from helpers.kolamPattern import KOLAM_CURVE_PATTERNS

# --- Direct connection lookups ---
pt_dn = [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1]
pt_rt = [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1]


def sort_by_origin(cells):
    return sorted(cells, key=lambda c: (c["x"]**2 + c["y"]**2))

def hasUnitCell(x, y, cells):
    return any(c["x"] == x and c["y"] == y for c in cells)

def get_cell(cells, x, y):
    for c in cells:
        if c["x"] == x and c["y"] == y:
            return c
    return None

def getValid(connB, connR):
    if not connB and not connR:
        return [1, 3, 4, 7]
    elif not connB and connR:
        return [5, 14]
    elif connB and not connR:
        return [2, 11, 13, 6]
    else:  # both True
        return [16, 9, 12, 15]

def generate_quadrant_pattern(unitCells, size, seed=None):
    if seed is not None:
        random.seed(seed)

    # lookup for quick existence check
    cells_set = {(c["x"], c["y"]) for c in unitCells}

    # start cell (closest to origin)
    start = min(unitCells, key=lambda c: (c["y"], c["x"]))
    start_x, start_y = start["x"], start["y"]

    # assign random pattern to start cell
    start_pattern = random.randint(1, 16)
    idx = start_pattern - 1
    start_cell = {
        "x": start_x,
        "y": start_y,
        "patternId": start_pattern,
        "connectedRight": bool(pt_rt[idx]),
        "connectedBottom": bool(pt_dn[idx])
    }

    generated = [start_cell]
    generated_map = {(start_x, start_y): start_cell}

    # row-by-row generation
    y = start_y
    while True:
        x = start_x
        row_generated = False
        while True:
            pos = (x, y)
            print(pos)
            if pos in generated_map:
                x += size
                continue
            print(pos)
            print(cells_set)

            if pos not in cells_set:
                print("broken")
                break  # stop this row when next point doesn’t exist

            # top neighbor
            top = generated_map.get((x, y - size))
            connB = top["connectedBottom"] if top else random.choice([True, False])
            print("connb",connB)

            # left neighbor
            left = generated_map.get((x - size, y))
            connR = left["connectedRight"] if left else random.choice([True, False])
            print("connrr",connR)

            # pick valid pattern
            valid_ids = getValid(connB, connR)
            print(valid_ids)
            chosen_id = random.choice(valid_ids)
            idx = chosen_id - 1

            # create the unit cell
            cell = {
                "x": x,
                "y": y,
                "patternId": chosen_id,
                "connectedRight": bool(pt_rt[idx]),
                "connectedBottom": bool(pt_dn[idx])
            }

            generated.append(cell)
            generated_map[pos] = cell
            row_generated = True

            x += size  # move right

        if not row_generated:
            break  # stop generation when no points exist in the next row
        y += size  # move down to next row

    return generated

