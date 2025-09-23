import pygame as pg
import sys

# Setup
pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("SAMOSA CLICKER")
FPS = pg.time.Clock()

# counter variable
click_count = 0

# Load image
samosa_original = pg.image.load("assets/samosa.png").convert_alpha()
samosa = samosa_original
samosa_rect = samosa.get_rect(center=(1280 // 2, 720 // 2))

# Setup font
font = pg.font.Font(None, 50)

# Predefine text position (above original samosa position)
text_pos = (samosa_rect.centerx, samosa_rect.top - 40)

# Scale effect
scale_up = False
scale_timer = 0
SCALE_DURATION = 150  # ms
SCALE_FACTOR = 1.1    # 110% size

# Game Loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # clicker counting (inside event loop!)
        if event.type == pg.MOUSEBUTTONDOWN:
            if samosa_rect.collidepoint(event.pos):
                click_count += 1
                print(click_count)
                # trigger scale-up effect
                scale_up = True
                scale_timer = pg.time.get_ticks()

    # Handle scaling
    if scale_up:
        elapsed = pg.time.get_ticks() - scale_timer
        if elapsed < SCALE_DURATION:
            # Scale up to 110% size
            new_size = (int(samosa_original.get_width() * SCALE_FACTOR),
                        int(samosa_original.get_height() * SCALE_FACTOR))
            samosa = pg.transform.smoothscale(samosa_original, new_size)
        else:
            # Reset to normal
            samosa = samosa_original
            scale_up = False

    # Keep samosa centered
    samosa_rect = samosa.get_rect(center=(1280 // 2, 720 // 2))

    # Fill background
    screen.fill((30, 30, 30))

    # Render text (fixed position, does not move)
    text_surface = font.render(f"Clicks: {click_count}", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, text_rect)

    # Draw samosa
    screen.blit(samosa, samosa_rect)

    # Update display
    pg.display.flip()
    FPS.tick(60)
