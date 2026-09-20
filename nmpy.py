import numpy as np
# Understanding dimensions
arr_1d = np.array([1, 2, 3, 4, 5])
arr_2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

print("1D Array:")
print(f"  {arr_1d} → shape: {arr_1d.shape}, ndim: {arr_1d.ndim} (axis 0 only)\n")

print("2D Array:")
print(f"  {arr_2d}")
print(f"  shape: {arr_2d.shape} (rows, columns)")
print(f"  ndim: {arr_2d.ndim} (axis 0=rows, axis 1=columns)")


# Axis in operations: specifies which dimension to collapse
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("Matrix:")
print(matrix)
print(f"Shape: {matrix.shape}\n")

# axis=0: collapse rows (operate down columns) → one value per column
sum_axis0 = np.sum(matrix, axis=0)
print(f"axis=0 (down rows): {sum_axis0}  → shape: {sum_axis0.shape}")
print(f"  Example: Column 0 sum = {matrix[0,0]} + {matrix[1,0]} + {matrix[2,0]} = {sum_axis0[0]}\n")

# axis=1: collapse columns (operate across rows) → one value per row
sum_axis1 = np.sum(matrix, axis=1)
print(f"axis=1 (across columns): {sum_axis1}  → shape: {sum_axis1.shape}")
print(f"  Example: Row 0 sum = {matrix[0,0]} + {matrix[0,1]} + {matrix[0,2]} = {sum_axis1[0]}\n")







# 3D Arrays: Axis with more than 2 dimensions
# Think: (depth, rows, columns) or (samples, height, width)
arr_3d = np.array([
    [[1, 2, 3],    # First 2D slice (page 0)
     [4, 5, 6]],
     
    [[7, 8, 9],    # Second 2D slice (page 1)
     [10, 11, 12]]
])

print("3D Array (shape: 2x2x3):")
print("Think: 2 pages, each with a 2x3 matrix")
print(arr_3d)
print(f"Shape: {arr_3d.shape}  (depth=2, rows=2, columns=3)\n")

# axis=0: collapse depth (across pages) → result: 2D (2×3)
sum_axis0 = np.sum(arr_3d, axis=0)
print(f"axis=0 (across pages):\n{sum_axis0}  → shape: {sum_axis0.shape}")
print(f"  Example: [0,0,0] = {arr_3d[0,0,0]} + {arr_3d[1,0,0]} = {sum_axis0[0,0]}\n")

# axis=1: collapse rows (down each page) → result: 2D (2×3)
sum_axis1 = np.sum(arr_3d, axis=1)
print(f"axis=1 (down rows):\n{sum_axis1}  → shape: {sum_axis1.shape}")
print(f"  Example: [0,0] = {arr_3d[0,0,0]} + {arr_3d[0,1,0]} = {sum_axis1[0,0]}\n")

# axis=2: collapse columns (across each row) → result: 2D (2×2)
sum_axis2 = np.sum(arr_3d, axis=2)
print(f"axis=2 (across columns):\n{sum_axis2}  → shape: {sum_axis2.shape}")
print(f"  Example: [0,0] = {arr_3d[0,0,0]} + {arr_3d[0,0,1]} + {arr_3d[0,0,2]} = {sum_axis2[0,0]}\n")
