"""
Pygame Basics 2: The Game Loop and Events
"""
import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Basics: The Game Loop")
clock = pygame.time.Clock()  # Controls frame rate

# Game State
box_x = 250
box_y = 150
speed = 5
color = (0, 0, 255)

running = True
while running:
    # ----------------------------------------
    # STEP 1: INPUT (Events)
    # ----------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Change color on spacebar press
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                color = (255, 0, 0) if color == (0, 0, 255) else (0, 0, 255)

    # Continuous keyboard input (holding down keys)
    keys = pygame.key.get_pressed()
    
    # ----------------------------------------
    # STEP 2: UPDATE (Game Logic)
    # ----------------------------------------
    if keys[pygame.K_LEFT]:
        box_x -= speed
    if keys[pygame.K_RIGHT]:
        box_x += speed
    if keys[pygame.K_UP]:
        box_y -= speed
    if keys[pygame.K_DOWN]:
        box_y += speed

    # Keep box on screen
    box_x = max(0, min(box_x, WIDTH - 50))
    box_y = max(0, min(box_y, HEIGHT - 50))

    # ----------------------------------------
    # STEP 3: RENDER (Drawing)
    # ----------------------------------------
    window.fill((255, 255, 255)) # Clear previous frame
    pygame.draw.rect(window, color, (box_x, box_y, 50, 50))
    pygame.display.flip()

    # Wait until next frame to maintain 60 FPS
    clock.tick(60)

pygame.quit()
sys.exit()
