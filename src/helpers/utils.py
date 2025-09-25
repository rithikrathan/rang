from helpers.type import CurvePoint
from helpers.kolamPattern import KOLAM_CURVE_PATTERNS
from p5 import *

def draw_pattern_at(x: float, y: float, pattern_id: int, size: float = 100):
    """Draw a kolam pattern centered at (x, y)."""
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

