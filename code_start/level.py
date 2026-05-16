from settings import *
from sprites import Sprite

class level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        self.setup(tmx_map)

        self.all_sprites = pygame.sprite.Group()

    def setup(self, tmx_map):
        for x, y, image in tmx_map.get_layer_by_name("Terrian").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)


    def run(self):
        self.display_surface.fill('gray')
        self.all_sprites.draw(self.display_surface)