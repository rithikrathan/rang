import threading
import tkinter as tk
from typing import List
from p5 import setup, draw, size, run, background, stroke, stroke_weight, line, ellipse, text, no_fill, fill

# --- Imports from helpers ---
from helpers.kolamPattern import KOLAM_CURVE_PATTERNS, SYMMETRY_TRANSFORMS, CONNECTIVITY_RULES
from helpers.kolamPattern import generate_compatibility_matrix

# --- Shared state ---
selected_pattern_id = 1
pattern_points: List = []
display_text: List[str] = []

# --- Precompute compatibility matrix ---
COMPATIBILITY_MATRIX = generate_compatibility_matrix()

print(COMPATIBILITY_MATRIX)


