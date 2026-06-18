from settings import * 
from math import sin, cos, radians

class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, surf=pg.Surface((TILE_SIZE, TILE_SIZE)), groups=(), z=Z_LAYERS["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = z

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z=Z_LAYERS["main"], animation_speed=ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)


class MovingSprite(AnimatedSprite):
    def __init__(self, frames, groups, start_pos, end_pos, move_dir, speed, flip=False):
        super().__init__(start_pos, frames, groups)
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

        self.flip = flip

        self.reverse = {"x" : False, "y" : False}

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
            self.reverse["x"] = True if self.dir.x < 0 else False
        else:
            # y-axis -> moving down
            if self.rect.bottom >= self.end_pos[1] and self.dir.y == 1:
                self.rect.bottom = self.end_pos[1]
                self.dir.y = -1 
            # y-axis - > moving up
            elif self.rect.top <= self.start_pos[1] and self.dir.y == -1:
                self.rect.top = self.start_pos[1]
                self.dir.y = 1 
            self.reverse["y"] = True if self.dir.x < 0 else False
 
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.dir * self.speed * dt
        self.check_border()
        self.animate(dt)
        if self.flip:
            self.image = pg.transform.flip(self.image, flip_x=self.reverse["x"], flip_y=self.reverse["y"])

class Spike(Sprite):
    def __init__(self, pos, surf, groups, radius, speed, start_angle, end_angle, z=Z_LAYERS["main"]):
        super().__init__(pos, surf, groups, z)
        self.center = pos
        self.radius = radius
        self.speed = speed
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.angle = self.start_angle
        self.direction = 1

        y = self.center[1] + sin(radians(self.angle)) * self.radius
        x = self.center[0] + cos(radians(self.angle)) * self.radius

        super().__init__((x, y), surf, groups, z)

    def check_angle(self):
        flip_dir = False
        if self.angle > self.end_angle: flip_dir = True
        elif self.angle < self.start_angle: flip_dir = True
        
        if flip_dir: self.direction *= -1

    def update(self, dt):
        self.check_angle()
        self.angle += self.speed * self.direction * dt
        y = self.center[1] + sin(radians(self.angle)) * self.radius
        x = self.center[0] + cos(radians(self.angle)) * self.radius
        self.rect.center = (x, y)

