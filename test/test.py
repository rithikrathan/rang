import threading
import tkinter as tk
from p5 import *

# Shared variables
radialSubdivision = 3
scaleFactor = 150
rotationAngle = 0
matrixDensity = 10

# p5 setup
def setup():
    size(400, 400)

def draw():
    global radialSubdivision
    global scaleFactor

    background(0)
    stroke(255)
    stroke_weight(1)
    no_fill()
    translate(width/2, height/2)
    rotate(radians(rotationAngle))
    
    vertices = []
    # calculate the angle between each radial subdivisions
    for i in range(radialSubdivision):
         angle = i * TWO_PI/radialSubdivision
         x =  scaleFactor * cos(angle)
         y =  scaleFactor * sin(angle)
         vertices.append((x,y))
    
    # draw lines for each subdivision from the center
    for x,y in vertices:
        line(0,0,x,y)

    for i in range(radialSubdivision):
        stroke(0,30,200)
        stroke_weight(2)
        
        x1,y1 = vertices[i]
        x2,y2 = vertices[(i +1) % radialSubdivision]
        line(x1,y1,x2,y2)
    stroke(255)
    stroke_weight(1)

# Tkinter UI
def tk_ui():
    global radialSubdivision
    global scaleFactor
    root = tk.Tk()
    root.title("Controls")

    # --- UI for radial subdivision ---
    tk.Label(root, text="Radial subdivision:").pack(anchor="w", pady=5)
    radialSubdivision_ui = tk.Spinbox(
        root, from_=1, to=300, width=5,
        command=lambda: update_values()
    )
    radialSubdivision_ui.delete(0, "end")
    radialSubdivision_ui.insert(0, str(radialSubdivision))
    radialSubdivision_ui.pack(anchor='w', pady=5)

    # --- UI for scale ---
    tk.Label(root, text="Size:").pack(anchor="w", pady=5)
    size_ui = tk.Spinbox(
        root, from_=10, to=300, width=5,
        command=lambda: update_values()
    )
    size_ui.delete(0, "end")
    size_ui.insert(0, str(scaleFactor))
    size_ui.pack(anchor="w", pady=5)

    # --- UI for rotation ---
    tk.Label(root, text="Rotation (in degrees):").pack(anchor="w", pady=5)
    rotationAngle_ui = tk.Spinbox(
        root, from_=5, to=300, width=5,increment=5,
        command=lambda: update_values()
    )
    rotationAngle_ui.delete(0, "end")
    rotationAngle_ui.insert(0, str(rotationAngle))
    rotationAngle_ui.pack(anchor="w", pady=5)

    # --- UI for matrix density
    tk.Label(root, text="Matrix density:").pack(anchor="w", pady=5)
    matrixDensity_ui = tk.Spinbox(
        root, from_=5, to=300, width=5,increment=5,
        command=lambda: update_values()
    )
    matrixDensity_ui.delete(0, "end")
    matrixDensity_ui.insert(0, str(matrixDensity))
    matrixDensity_ui.pack(anchor="w", pady=5)

    def update_values(event=None):
        global scaleFactor
        global radialSubdivision
        global rotationAngle
        try:
            scaleFactor = int(size_ui.get())
            radialSubdivision = int(radialSubdivision_ui.get())
            rotationAngle = int(rotationAngle_ui.get())
        except ValueError:
            pass  # ignore invalid input

    # Update when Enter is pressed (fix: no parentheses!)
    radialSubdivision_ui.bind("<Return>", update_values)
    size_ui.bind("<Return>", update_values)

    root.mainloop()



# Run Tkinter in a separate thread
threading.Thread(target=tk_ui, daemon=True).start()

# Start p5 loop
run()
