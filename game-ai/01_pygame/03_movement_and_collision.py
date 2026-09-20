"""
Pygame Basics 3: Movement and Collision
"""
import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Basics: Collision")
clock = pygame.time.Clock()

# A pygame.Rect stores x, y, width, and height. 
# It provides highly optimized collision math.
player_rect = pygame.Rect(50, 150, 50, 50)
enemy_rect = pygame.Rect(400, 150, 60, 100)
enemy_speed_y = 3

running = True
while running:
    # --- INPUT ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # --- UPDATE ---
    # Move Player
    if keys[pygame.K_LEFT]: player_rect.x -= 5
    if keys[pygame.K_RIGHT]: player_rect.x += 5
    if keys[pygame.K_UP]: player_rect.y -= 5
    if keys[pygame.K_DOWN]: player_rect.y += 5

    # Move Enemy (bouncing up and down)
    enemy_rect.y += enemy_speed_y
    if enemy_rect.bottom >= HEIGHT or enemy_rect.top <= 0:
        enemy_speed_y *= -1 # Reverse direction

    # Collision Detection
    # .colliderect() returns True if two rectangles overlap
    if player_rect.colliderect(enemy_rect):
        player_color = (255, 0, 0) # Red if hitting
    else:
        player_color = (0, 255, 0) # Green if safe

    # --- RENDER ---
    window.fill((30, 30, 30))
    pygame.draw.rect(window, player_color, player_rect)
    pygame.draw.rect(window, (200, 200, 200), enemy_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
