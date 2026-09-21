from pathlib import Path

BASE_DIR = Path("/home/settings/Documents/pearl/engineering-mathematics")

trig_dir = BASE_DIR / "trigonometry"
trig_dir.mkdir(exist_ok=True)

with open(trig_dir / "README.md", "w") as f:
    f.write("""# Trigonometry

## Intuition: What is an Angle?
An angle represents a rotation or a direction. 
* **Degrees**: 360 degrees in a full circle. (Used in human navigation).
* **Radians**: 2π radians in a full circle. (Used in calculus because it simplifies derivatives).

## The Unit Circle
Imagine a circle with radius 1.
* **cos(θ)**: The x-coordinate of the point on the circle.
* **sin(θ)**: The y-coordinate of the point on the circle.

## Right-Triangle Relationships
```text
sin(θ) = opposite / hypotenuse
cos(θ) = adjacent / hypotenuse
```
Let's derive **tan(θ)**:
```text
tan(θ) = sin(θ) / cos(θ)
       = (opposite / hypotenuse) / (adjacent / hypotenuse)
       = opposite / adjacent
```

## Connections to Later Courses

### Programming & Pygame
To move an agent smoothly in a 2D game in direction θ:
```python
x_velocity = speed * math.cos(theta)
y_velocity = speed * math.sin(theta)
```

### Machine Learning
Trigonometric functions appear in mathematical models and periodic feature representations (like Positional Encoding in Transformers), allowing the neural network to understand repeating patterns.

### Engineering
Used heavily in AC signals, oscillations, and wave analysis.
""")

with open(trig_dir / "trig_demo.py", "w") as f:
    f.write("""import math

theta_radians = math.pi / 4 # 45 degrees

# Calculate movement vector
speed = 10
vx = speed * math.cos(theta_radians)
vy = speed * math.sin(theta_radians)

print(f"Angle: {math.degrees(theta_radians)} degrees")
print(f"Velocity vector: (vx: {vx:.2f}, vy: {vy:.2f})")
""")

print("Trigonometry added.")
