import threading
import tkinter as tk
from dataclasses import dataclass
from p5 import *
from helpers.kolamGen import fillAxis
from helpers.polygonUtils import *
from helpers.kolamGen import *
from helpers.kolamPattern import *
from helpers.utils import *


@dataclass
class int2d:
    x: int
    y: int


# Shared variables (with initial values)
matrixDensity = 27
matrixBounds = 1
radialSubdivision = 4
bounds = (300, 300)
scaleFactor = int2d(x=200, y=200)
rotationAngle = 0
seed = 245

# boolean vars
enableBounds = False
enableSegments = False
enableVertices = False
enableMatrix = True
evenMatrix = False
enablePattern = True

polygonVertices = []
guidePoints = []

unitCells = []

# objects
transform = Transform()
pointTools = pointTools()

# p5 setup


def setup():  # runs on startup
    onValues_changed()
    size(450, 450)


def draw():  # runs every frame
    # variables and stuffs
    global radialSubdivision
    global matrixDensity
    global polygonVertices
    global guidePoints
    global scaleFactor
    global update
    global unitCells

    background(0)
    stroke(255)
    stroke_weight(1)
    no_fill()
    translate(width/2, height/2)
    # onValues_changed()

    # actual stuffs that draws something on the screen
    if enablePattern:
        for unitCell in unitCells:
            draw_pattern_at(unitCell, size=matrixDensity)

    if enableSegments:
        # draw lines for each subdivision from the center
        stroke(0, 130, 130)
        for x, y in polygonVertices:
            line(0, 0, x, y)
        stroke(255)

    if enableBounds:
        for i in range(radialSubdivision):
            stroke(0, 30, 200)
            stroke_weight(2)

            x1, y1 = polygonVertices[i]
            x2, y2 = polygonVertices[(i + 1) % radialSubdivision]
            line(x1, y1, x2, y2)
        stroke(255)
        stroke_weight(1)

    # --- Draw vertex coordinates ---
    if enableVertices:
        fill(255)
        for (x, y) in polygonVertices:
            stroke(0, 255, 0)
            stroke_weight(5)
            point(x, y)
            stroke(255, 30, 30)
            point(0, 0)
            stroke(255)
            stroke_weight(1)
            text(f"({int(x)}, {int(y)})", x + 5, y - 5)

    if enableMatrix:
        for (x, y) in guidePoints:
            stroke(255, 255, 255)
            stroke_weight(3)
            point(x, y)
            stroke(0, 255, 0)
            stroke_weight(1)


# Tkinter UI
def tk_ui():
    global radialSubdivision
    global scaleFactor
    root = tk.Tk()
    root.title("Controls")

    # --- UI for boolean option ---
    tk.Label(root, text="Boolean Variables:").pack(anchor="w")

    enableBounds_buf = tk.BooleanVar(value=enableBounds)
    enableBounds_ui = tk.Checkbutton(root, text='enableBounds',
                                     variable=enableBounds_buf,
                                     command=lambda: update_values())
    enableBounds_ui.pack(anchor="w", pady=1)

    enableSegments_buf = tk.BooleanVar(value=enableSegments)
    enableSegments_ui = tk.Checkbutton(root, text='enableSegments',
                                       variable=enableSegments_buf,
                                       command=lambda: update_values())
    enableSegments_ui.pack(anchor="w", pady=1)

    enableVertices_buf = tk.BooleanVar(value=enableVertices)
    enableVertices_ui = tk.Checkbutton(root, text='enableVertices',
                                       variable=enableVertices_buf,
                                       command=lambda: update_values())
    enableVertices_ui.pack(anchor="w", pady=1)

    enableMatrix_buf = tk.BooleanVar(value=enableMatrix)
    enableMatrix_ui = tk.Checkbutton(root, text='enableMatrix',
                                     variable=enableMatrix_buf,
                                     command=lambda: update_values())
    enableMatrix_ui.pack(anchor="w", pady=1)

    evenMatrix_buf = tk.BooleanVar(value=evenMatrix)
    evenMatrix_ui = tk.Checkbutton(root, text='evenMatrix',
                                   variable=evenMatrix_buf,
                                   command=lambda: update_values())
    evenMatrix_ui.pack(anchor="w", pady=1)

    enablePattern_buf = tk.BooleanVar(value=enablePattern)
    enablePattern_ui = tk.Checkbutton(root, text='enablePattern',
                                      variable=enablePattern_buf,
                                      command=lambda: update_values())
    enablePattern_ui.pack(anchor="w", pady=1)

    # --- UI for radial subdivision ---
    tk.Label(root, text="Radial subdivision:").pack(anchor="w")
    radialSubdivision_ui = tk.Spinbox(
        root, from_=1, to=15, width=5,
        command=lambda: update_values()
    )
    radialSubdivision_ui.delete(0, "end")
    radialSubdivision_ui.insert(0, str(radialSubdivision))
    radialSubdivision_ui.pack(anchor='w', pady=1)

    # --- UI for horizontal scale ---
    tk.Label(root, text="Scale X:").pack(anchor="w", pady=5)
    scale_x_ui = tk.Spinbox(root, from_=10, to=300, width=5,
                            command=lambda: update_values())
    scale_x_ui.delete(0, "end")
    scale_x_ui.insert(0, str(scaleFactor.x))
    scale_x_ui.pack(anchor="w", pady=1)

    # --- UI for vertical scale ---
    tk.Label(root, text="Scale Y:").pack(anchor="w", pady=5)
    scale_y_ui = tk.Spinbox(root, from_=10, to=300, width=5,
                            command=lambda: update_values())
    scale_y_ui.delete(0, "end")
    scale_y_ui.insert(0, str(scaleFactor.y))
    scale_y_ui.pack(anchor="w", pady=1)

    # --- UI for rotation ---
    tk.Label(root, text="Rotation (in degrees):").pack(anchor="w")
    rotationAngle_ui = tk.Spinbox(
        root, from_=0, to=360, width=5, increment=1,
        command=lambda: update_values()
    )
    rotationAngle_ui.delete(0, "end")
    rotationAngle_ui.insert(0, str(rotationAngle))
    rotationAngle_ui.pack(anchor="w", pady=1)

    # --- UI for matrix density
    tk.Label(root, text="Matrix density X:").pack(anchor="w")
    matrixDensity_ui = tk.Spinbox(
        root, from_=5, to=300, width=5, increment=1,
        command=lambda: update_values()
    )
    matrixDensity_ui.delete(0, "end")
    matrixDensity_ui.insert(0, str(matrixDensity))
    matrixDensity_ui.pack(anchor="w", pady=1)

    # --- UI for matrixBounds
    tk.Label(root, text="Matrix bounds:").pack(anchor="w")
    matrixBounds_ui = tk.Spinbox(
        root, from_=1, to=4, width=5, increment=1,
        command=lambda: update_values()
    )
    matrixBounds_ui.delete(0, "end")
    matrixBounds_ui.insert(0, str(matrixBounds))
    matrixBounds_ui.pack(anchor="w", pady=1)

    # --- tkui for random seed
    tk.Label(root, text="Random seed:").pack(anchor="w")
    seed_ui = tk.Spinbox(
        root, from_=1, to=999999, width=5, increment=1,
        command=lambda: update_values()
    )
    seed_ui.delete(0, "end")
    seed_ui.insert(0, str(seed))
    seed_ui.pack(anchor="w", pady=1)

    def update_values(event=None):
        global scaleFactor
        global radialSubdivision
        global rotationAngle
        global evenMatrix
        global enableSegments
        global enableMatrix
        global enableVertices
        global enableBounds
        global matrixDensity
        global matrixBounds
        global enablePattern
        global seed

        try:
            scaleFactor.x = int(scale_x_ui.get())
            scaleFactor.y = int(scale_y_ui.get())
            radialSubdivision = int(radialSubdivision_ui.get())
            rotationAngle = int(rotationAngle_ui.get())
            matrixDensity = int(matrixDensity_ui.get())
            matrixBounds = int(matrixBounds_ui.get())
            seed = int(seed_ui.get())
            evenMatrix = evenMatrix_buf.get()
            enableBounds = enableBounds_buf.get()
            enableSegments = enableSegments_buf.get()
            enableVertices = enableVertices_buf.get()
            enableMatrix = enableMatrix_buf.get()
            enablePattern = enablePattern_buf.get()
            onValues_changed()
        except ValueError:
            print("Owned by skill issue")
            pass  # ignore invalid input

    # Call update on any Enter press
    root.bind("<Return>", update_values)
    root.mainloop()


def generatePoints(point, density, points, polygon, visited=None):
    # with point as the origin recursively generate 4 points, one in every direction
    # idgaf if this is expensive i just want it to work
    # fuck the space complixity readablity is what i need right now

    # probably make this iterative so you wont have to worry about the 
    # maximum recursion depth and stuffs, using a queue instead of the stack memory
    # same time complexity but no maximum recursion depth error

    if visited is None:
        visited = set()

    x, y = point

    if point in visited:
        return
    visited.add(point)

    if pointTools.containedIn(polygon, point):
        points.append(point)
    else:
        return

    generatePoints((x, y + density), density, points, polygon, visited)
    generatePoints((x, y - density), density, points, polygon, visited)
    generatePoints((x + density, y), density, points, polygon, visited)
    generatePoints((x - density, y), density, points, polygon, visited)


def onValues_changed():
    # Math stuffs
    global polygonVertices
    global guidePoints
    global unitCells
    global matrixBounds
    global matrixDensity

    polygonVertices = []
    guidePoints = []
    unitCells = []

    # calculate the angle between each radial subdivision
    for i in range(radialSubdivision):
        angle = i * TWO_PI / radialSubdivision
        x = scaleFactor.x * cos(angle)
        y = scaleFactor.y * sin(angle)
        x, y = transform.rotate(x, y, rotationAngle)
        polygonVertices.append((x, y))

    # recursively generate the matrices (points to place unitcells)
    if evenMatrix:
        origin = (matrixDensity/2, matrixDensity/2)
        generatePoints(origin, matrixDensity, guidePoints,
                       polygonVertices)
    else:
        origin = (0, 0)
        generatePoints(origin, matrixDensity, guidePoints,
                       polygonVertices)

    # initially place a unit cell with a circle pattern in every point in the matrix
    for point in guidePoints:
        unitCell = {"x": point[0], "y": point[1], "patternId": 1,
                    "connectedRight": False, "connectedBottom": False}
        unitCells.append(unitCell)

    # filter the matrix to keep only one quadrant to generate a symmetric
    # mirror images in all other quadrants
    filterByQuadrant(unitCells, matrixBounds)

    unitCells = generate_quadrant_pattern(unitCells, matrixDensity, seed)


    if not evenMatrix:
        axisFills = fillAxis(unitCells,guidePoints,matrixDensity,seed)
        for i in axisFills:
            unitCells.append(i)

    unitCells = mirrorVertical(unitCells)
    unitCells = mirrorHorizontal(unitCells)

# Run Tkinter in a separate thread
threading.Thread(target=tk_ui, daemon=True).start()

# Start p5 loop
run()
