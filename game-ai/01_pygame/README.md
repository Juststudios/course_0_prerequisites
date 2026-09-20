# Module 1: Pygame Fundamentals

## What is Pygame?
Pygame is a set of Python modules designed for writing video games. It provides tools for:
* **Rendering:** Drawing shapes, images, and text to a screen.
* **Input Handling:** Reading the keyboard and mouse.
* **Audio:** Playing sounds and music.
* **Timing:** Controlling the frame rate (FPS).

Why use a game library? Writing graphics directly to a screen buffer or reading raw hardware inputs is extremely complex. Pygame handles the low-level hardware communication so you can focus on the game logic.

## The Game Loop
Every real-time game, from Pong to modern 3D titles, runs on a fundamental loop that repeats dozens of times per second:

```text
Input (Check keyboard/mouse)
 ↓
Update (Move characters, check collisions)
 ↓
Render (Draw the new frame to the screen)
 ↓
Repeat
```

## Exploring the Basics

We have broken down the Pygame fundamentals into three progressive scripts. Run them and study the code:

### 1. `01_basics.py`
Teaches how to initialize Pygame, create a window, define colors using RGB, and draw basic shapes (rectangles, circles, lines).

### 2. `02_game_loop.py`
Introduces the Pygame event queue (how to detect when the user clicks the "X" to quit or presses a key) and the `Clock` object to maintain a steady 60 Frames Per Second (FPS).

### 3. `03_movement_and_collision.py`
Introduces coordinates (X, Y), bounding boxes (`pygame.Rect`), moving objects around the screen, and detecting when two objects collide.

---

## Important Coordinate Concept
In standard mathematics (Cartesian coordinates), `Y` goes UP.
In almost all computer graphics (including Pygame), **`Y` goes DOWN**.
* Top-Left corner is `(0, 0)`
* Bottom-Right corner is `(WIDTH, HEIGHT)`

## What You Should Know Before Moving On
* How to start and safely quit a Pygame window.
* What the Game Loop is (Input -> Update -> Render).
* How to draw a rectangle and move it using variables.
