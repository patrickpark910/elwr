import numpy as np

# Define the step and grid size
step = 1.25
size = 4*17

# Calculate the range of values centered around zero
offsets = np.linspace(-step * (size // 2), step * (size // 2), size)

# Generate the grid of points
points = np.array(np.meshgrid(offsets, offsets)).T.reshape(-1, 2)

# Format and print each coordinate pair
points_formatted = "\n".join(f"{(x+0.6425):.4f} {(y+0.6425):.4f} 0" for x, y in points)
print(points_formatted)
