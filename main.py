import pygame as pg
import sys

# Setup
pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption("Hello World!")
FPS = pg.time.Clock()

# Game Loop
while True:
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    FPS.tick(60)

    pg.display.flip()