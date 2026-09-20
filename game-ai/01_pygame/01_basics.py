"""
Pygame Basics 1: Window and Drawing
"""
import pygame
import sys

# 1. Initialize Pygame
pygame.init()

# 2. Setup the display
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Basics: Drawing")

# 3. Define Colors (R, G, B) - 0 to 255
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 4. Fill the background
window.fill(WHITE)

# 5. Draw Shapes
# pygame.draw.rect(surface, color, (x, y, width, height))
pygame.draw.rect(window, RED, (50, 50, 100, 50))

# pygame.draw.circle(surface, color, (center_x, center_y), radius)
pygame.draw.circle(window, BLUE, (300, 200), 50)

# pygame.draw.line(surface, color, start_pos, end_pos, width)
pygame.draw.line(window, GREEN, (0, 0), (WIDTH, HEIGHT), 5)

# 6. Update the display (Pygame draws to a hidden buffer, this swaps it to the screen)
pygame.display.flip()

# 7. A very basic event loop just to keep the window open until we click X
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
