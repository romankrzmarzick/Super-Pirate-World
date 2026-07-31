from settings import ANIMATION_SPEED, pygame, HEART_PADDING
from sprites import AnimatedSprite
from random import randint
from time_track import Timer


class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font
    
        # helath
        self.heart_frames = frames["heart"]
        self.coin_image = frames['coin']
        self.heart_surf_width = self.heart_frames[0].get_width()

        self.heart_padding: int = HEART_PADDING
        
        # coins
        self.coin_amount: int = 0
        self.coin_timer = Timer(1000)


    def create_hearts(self, amount: int):
        for sprite in self.sprites:
            if hasattr(sprite, 'heart'): sprite.kill()
        for heart in range(amount):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x,y), self.heart_frames, self.sprites)

    def display_text(self):
        text_surf = self.font.render(str(self.coin_amount), False, '#33323d')
        text_rect: pygame.FRect = text_surf.get_frect(topleft=(16,34))
        self.display_surface.blit(text_surf, text_rect)

        coin_rect = self.coin_image.get_frect(center=text_rect.bottomleft).move(0, -4)
        self.display_surface.blit(self.coin_image, coin_rect)

    def show_coins(self, amount: int):
        self.coin_amount = amount
        self.coin_timer.activate()


    def update(self, dt: float) -> None:
        self.coin_timer.update()
        self.sprites.update(dt)
        self.sprites.draw(self.display_surface)
        if self.coin_timer.active:
            self.display_text()

class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active: bool = False
        self.heart: bool = True

    def animate(self, dt: float):
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0

    def update(self, dt: float):
        if self.active:
            self.animate(dt)
        else:
            if randint(0, 2000) == 1:
                self.active = True
