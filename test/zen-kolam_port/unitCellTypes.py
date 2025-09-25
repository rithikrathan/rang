import threading
import tkinter as tk
from p5 import *
from type import CurvePoint
from kolamPattern import KOLAM_CURVE_PATTERNS

# --- Shared state ---
selected_pattern_id = 1
pattern_points = []

# --- p5 drawing ---
def setup():
    size(400, 400)
    no_fill()
    stroke(255)


def draw():
    background(0)
    translate(width / 2, height / 2)

    if not pattern_points:
        return

    # Determine bounds
    xs = [p.x for p in pattern_points]
    ys = [p.y for p in pattern_points]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    pattern_width = max_x - min_x
    pattern_height = max_y - min_y

    # Compute scaling factor to fit canvas
    scale_x = (width * 0.8) / pattern_width if pattern_width != 0 else 1
    scale_y = (height * 0.8) / pattern_height if pattern_height != 0 else 1
    scale_factor = min(scale_x, scale_y)

    # Center pattern
    cx = (max_x + min_x) / 2
    cy = (max_y + min_y) / 2

    stroke(255)
    stroke_weight(2)
    begin_shape()
    for p in pattern_points:
        px = (p.x - cx) * scale_factor
        py = (p.y - cy) * scale_factor
        vertex(px, py)
    end_shape(CLOSE)

    # Draw dot at origin
    fill(255, 0, 0)
    circle((0, 0), 6)


# --- Tkinter UI ---
def tk_ui():
    global selected_pattern_id

    root = tk.Tk()
    root.title("Kolam Pattern Selector")

    tk.Label(root, text="Pattern ID (1–16):").pack(anchor="w")
    kolam_var = tk.IntVar(value=selected_pattern_id)

    def update_pattern():
        global pattern_points
        selected_pattern_id = kolam_var.get()
        pat = next((p for p in KOLAM_CURVE_PATTERNS if p.id == selected_pattern_id), None)
        if pat:
            # mutate the existing list
            pattern_points.clear()
            pattern_points.extend([
                CurvePoint(x=pt[0], y=pt[1]) if isinstance(pt, list)
                else CurvePoint(x=pt["x"], y=pt["y"])
                for pt in pat.points
                ])
        else:
            pattern_points.clear()

    spin = tk.Spinbox(root, from_=1, to=16, width=5, textvariable=kolam_var, command=update_pattern)
    spin.pack(anchor="w")

    # initial load
    update_pattern()

    root.mainloop()


# --- Run Tkinter in a thread ---
threading.Thread(target=tk_ui, daemon=True).start()

# --- Run p5 sketch ---
run()

