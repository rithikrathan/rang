from helpers.kolamPattern import KOLAM_CURVE_PATTERNS, SYMMETRY_TRANSFORMS
from helpers.type import *
from p5 import *
import math
import random


def draw_pattern_at(unitCell, size: float = 100):
    x = unitCell["x"]
    y = unitCell["y"]
    pattern_id = unitCell["patternId"]
    # to make these tile with each other
    if pattern_id == 1: # circl
        size = size // 1.5
    elif pattern_id == 2: # connected up
        y = y - size / 12
    elif pattern_id == 13:
        x = x + size / 7
    elif pattern_id == 15:
        x = x - size / 7
    elif pattern_id == 14:
        y = y + size / 7
    elif pattern_id == 12:
        y = y - size / 7
    elif pattern_id == 6: #catEars_bl
        x = x + size / 10
        y = y - size / 10
        size = size // 1.25
    elif pattern_id == 9: #catEars_br
        x = x - size / 10
        y = y - size / 10
        size = size // 1.25
    elif pattern_id == 7: #catEars_tl
        x = x + size / 10
        y = y + size / 10
        size = size // 1.25
    elif pattern_id == 8: #catEars_tr
        x = x - size / 10
        y = y + size / 10
        size = size // 1.25


    pat = next((p for p in KOLAM_CURVE_PATTERNS if p.id == pattern_id), None)
    if not pat:
        return

    pts = [
        CurvePoint(pt[0], pt[1]) if isinstance(pt, list)
        else CurvePoint(pt["x"], pt["y"])
        for pt in pat.points
    ]

    if not pts:
        return

    xs = [p.x for p in pts]
    ys = [p.y for p in pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    w, h = max_x - min_x, max_y - min_y
    scale_factor = size / max(w, h) if max(w, h) != 0 else 1
    cx, cy = (max_x + min_x) / 2, (max_y + min_y) / 2

    push_matrix()
    translate(x, y)
    no_fill()
    stroke(255)
    stroke_weight(2)
    begin_shape()
    for p in pts:
        px = (p.x - cx) * scale_factor
        py = (p.y - cy) * scale_factor
        vertex(px, py)
    end_shape(CLOSE)
    pop_matrix()


def filterByQuadrant(cells, quad):
    if quad == 1:
        cells[:] = [p for p in cells if p["x"] > 0 and p["y"] > 0]
    elif quad == 2:
        cells[:] = [p for p in cells if p["x"] < 0 and p["y"] > 0]
    elif quad == 3:
        cells[:] = [p for p in cells if p["x"] < 0 and p["y"] < 0]
    elif quad == 4:
        cells[:] = [p for p in cells if p["x"] > 0 and p["y"] < 0]
    else:
        raise ValueError("quad must be 1, 2, 3, or 4")

    cells.sort(key=lambda p: math.atan2(p["y"], p["x"]))


def mirrorVertical(cells):
    mirrored = []
    for cell in cells:
        old_id = cell["patternId"]
        new_id = SYMMETRY_TRANSFORMS["horizontalInverse"][old_id - 1]

        mirrored.append({
            **cell,
            "x": -cell["x"],   # flip x
            "patternId": new_id
        })

    cells.extend(mirrored)
    return cells


def mirrorHorizontal(cells):
    mirrored = []
    for cell in cells:
        old_id = cell["patternId"]
        new_id = SYMMETRY_TRANSFORMS["verticalInverse"][old_id - 1]

        mirrored.append({
            **cell,
            "y": -cell["y"],   # flip x
            "patternId": new_id
        })

    cells.extend(mirrored)
    return cells


def rotate_90(cells):
    rotated = []
    for cell in cells:
        old_id = cell["patternId"]
        new_id = SYMMETRY_TRANSFORMS["rotation90"][old_id - 1]  # map patternId

        rotated.append({
            **cell,
            "x": -cell["y"],   # (x, y) -> (-y, x)
            "y": cell["x"],
            "patternId": new_id
        })
    return rotated


def generatePattern(cells, seed=None):
    if seed is not None:
        random.seed(seed)

    # Assign patternIds
    for cell in cells:
        # Example: pick patternId randomly from 1 to 16
        cell["patternId"] = random.randint(1, 16)

    return cells
