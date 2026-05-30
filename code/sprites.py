
from typing import Any

from settings import * 

class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, groups, surf=pg.Surface((TILE_SIZE, TILE_SIZE)), z=Z_LAYERS["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = z

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z=Z_LAYERS["main"], animation_speed=ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, groups, surf=self.frames[self.frame_index])
        self.animation_speed = animation_speed
    
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, dt):
        self.animate(dt)


class MovingSprite(Sprite):
    def __init__(self, groups, start_pos, end_pos, move_dir, speed):
        surf = pg.Surface((200, 50))
        super().__init__(start_pos, groups, surf)
        self.image.fill((255, 255, 255))
        # // rect alignment
        if move_dir == "x":
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos
        
        # // path
        self.rect.center = start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos

        # // movement
        self.moving = True
        self.speed = speed
        self.dir = vector(1, 0) if move_dir == "x" else vector(0, 1)
        self.move_dir = move_dir

    def check_border(self):
        # // border rules
        if self.move_dir == "x":
            # x-axis -> moving right
            if self.rect.right >= self.end_pos[0] and self.dir.x == 1:
                self.rect.right = self.end_pos[0]
                self.dir.x = -1 
            # x-axis -> moving left
            elif self.rect.left <= self.start_pos[0] and self.dir.x == -1:
                self.rect.left = self.start_pos[0]
                self.dir.x = 1 
        else:
            # y-axis -> moving down
            if self.rect.bottom >= self.end_pos[1] and self.dir.y == 1:
                self.rect.bottom = self.end_pos[1]
                self.dir.y = -1 
            # y-axis - > moving up
            elif self.rect.top <= self.start_pos[1] and self.dir.y == -1:
                self.rect.top = self.start_pos[1]
                self.dir.y = 1 
 
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.dir * self.speed * dt
        self.check_border()

