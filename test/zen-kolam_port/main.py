import threading
import tkinter as tk
from type import Dot, Line, CurvePoint, KolamPattern
from kolam import KolamGenerator
from kolamPattern import KOLAM_CURVE_PATTERNS
from p5 import setup, draw, size, background, stroke, stroke_weight, line as p5_line, ellipse, run, no_fill

CELL_SPACING = KolamGenerator.CELL_SPACING
pattern = None
kolam_size = 5  # default size

# Convert JSON points to CurvePoint
for pat in KOLAM_CURVE_PATTERNS:
    if pat.points and not isinstance(pat.points[0], CurvePoint):
        pat.points = [
            CurvePoint(
                x=p['x'],
                y=p['y'],
                controlX=p.get('controlX'),
                controlY=p.get('controlY')
            )
            for p in pat.points
        ]


def regenerate_kolam():
    global pattern
    pattern = KolamGenerator.generate_kolam_1d(kolam_size_var.get())
    print(f"Generated Kolam {kolam_size_var.get()}x{kolam_size_var.get()}")

# --- Tkinter GUI in separate thread ---


def tk_thread():
    global kolam_size_var
    root = tk.Tk()
    root.title("Kolam Generator")

    tk.Label(root, text="Kolam Size:").grid(row=0, column=0, padx=5, pady=5)
    kolam_size_var = tk.IntVar(value=kolam_size)
    size_entry = tk.Spinbox(root, from_=1, to=20,
                            textvariable=kolam_size_var, width=5)
    size_entry.grid(row=0, column=1, padx=5, pady=5)

    generate_btn = tk.Button(
        root, text="Regenerate Kolam", command=regenerate_kolam)
    generate_btn.grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()


# Start Tkinter in a thread
threading.Thread(target=tk_thread, daemon=True).start()

# --- p5 setup ---


def setup():
    global pattern
    w, h = 600, 600
    size(w, h)
    background(0)
    no_fill()
    # generate initial pattern
    pattern = KolamGenerator.generate_kolam_1d(kolam_size)


def draw():
    global pattern
    if pattern is None:
        return
    background(0)
    stroke(255)
    stroke_weight(1.5)
    for curve in pattern.curves:
        pts = curve.curvePoints
        for i in range(len(pts)-1):
            p5_line((pts[i].x, pts[i].y), (pts[i+1].x, pts[i+1].y))
    stroke(255)
    stroke_weight(3)
    for dot in pattern.dots:
        ellipse((dot.center.x, dot.center.y), dot.radius, dot.radius)


run()
