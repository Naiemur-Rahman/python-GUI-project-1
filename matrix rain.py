import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
FONT_SIZE = 18
COLUMNS = int(WIDTH // (FONT_SIZE * 1.5))

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Matrix Rain - Naiem")

# Font setup (Anti-Aliased)
font = pygame.font.SysFont("Courier", FONT_SIZE, bold=True)
title_font = pygame.font.SysFont("Courier New", 80, bold=True)  # High-quality font

# Raindrop positions and trail effect
drops = [{'y': random.randint(0, HEIGHT), 'trail': []} for _ in range(COLUMNS)]

# Title animation settings
title = "Naiem"
title_size = 0
title_max_size = 100
title_growth = 0.5

# Main loop
clock = pygame.time.Clock()
running = True
start_time = pygame.time.get_ticks()

while running:
    screen.fill(BLACK)

    # Get elapsed time
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

    # Matrix rain effect
    for i, drop in enumerate(drops):
        x = i * FONT_SIZE * 1.5
        y = drop['y']

        # Add new character to the trail
        char = chr(random.randint(33, 126))
        drop['trail'].append((x, y, char))

        # Control trail length
        if len(drop['trail']) > 15:
            drop['trail'].pop(0)

        # Draw fading trail effect
        for j, (tx, ty, tchar) in enumerate(drop['trail']):
            alpha = int(255 * (j / len(drop['trail'])))
            color = (0, alpha, 0)
            text = font.render(tchar, True, color)
            screen.blit(text, (tx, ty))

        # Move drop down, reset if off-screen
        if y > HEIGHT and random.random() > 0.975:
            drop['y'] = 0
            drop['trail'] = []  
        else:
            drop['y'] += FONT_SIZE

    # Title animation (Smooth scaling)
    if elapsed_time > 3:
        if title_size < title_max_size:
            title_size += title_growth + (title_max_size - title_size) * 0.05  # Smooth acceleration

        # Create depth shadow effect
        shadow_surface = title_font.render(title, True, DARK_GREEN)
        shadow_surface = pygame.transform.scale(shadow_surface, (int(title_size * 4), int(title_size)))
        screen.blit(shadow_surface, shadow_surface.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 3 + 3)))

        # High-quality text render with Anti-Aliasing
        title_surface = title_font.render(title, True, GREEN)
        title_surface = pygame.transform.scale(title_surface, (int(title_size * 4), int(title_size)))
        screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3)))

    # Update display
    pygame.display.flip()
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

