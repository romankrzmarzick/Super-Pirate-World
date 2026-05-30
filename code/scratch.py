from settings import * 
import pygame
from support import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((960, 540))
clock = pygame.time.Clock()

# imports 
surf = import_image("graphics", "player", "idle", "0")
surf_list = import_folder("graphics", "player", "attack")
surf_folder = import_sub_folders("graphics", "player")
tile_surfs = import_tile_map(2, 3, "graphics", "tilesets", "items")

print(tile_surfs)

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # render
    screen.fill("grey")
    screen.blit(surf, (75, 75))
    
    screen.blit(surf_list[0], (300, 50))
    screen.blit(surf_list[1], (200, 75))
    screen.blit(surf_list[2], (200, 200))
    screen.blit(tile_surfs[(0, 2)], (400, 300))

    pygame.display.flip()

pygame.quit()