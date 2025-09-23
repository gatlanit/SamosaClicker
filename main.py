import pygame as pg
import sys

# Setup
pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("Hello World!")
FPS = pg.time.Clock()

# Load image
samosa = pg.image.load(
    "assets/samosa.png"
).convert_alpha()  # use convert_alpha if transparency
samosa_rect = samosa.get_rect(center=(1280 // 2, 720 // 2))

# Game Loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Fill background (optional, prevents trails)
    screen.fill((30, 30, 30))

    # Draw image at the center
    screen.blit(samosa, samosa_rect)

    # Update display
    pg.display.flip()
    FPS.tick(60)
