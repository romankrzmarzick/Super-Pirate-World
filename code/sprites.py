from typing import Any

from pygame import Surface

from settings import * 
from math import sin, cos, radians

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, surf: pygame.Surface=pygame.Surface((TILE_SIZE, TILE_SIZE)), groups=(), z=Z_LAYERS["main"]):
        super().__init__(groups)
        self.image: pygame.Surface = surf
        self.rect: pygame.FRect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = z

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z=Z_LAYERS["main"], animation_speed=ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed: int = animation_speed

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)

class Item(AnimatedSprite):
    def __init__(self, item_type: str, pos, frames, groups, storage):
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.item_type = item_type
        self.storage = storage

    def activate(self):
        if self.item_type == 'gold':
            self.storage.coins += 5
        if self.item_type == 'silver':
            self.storage.coins += 1
        if self.item_type == 'diamond':
            self.storage.coins += 20
        if self.item_type == 'skull':
            self.storage.coins += 50
        if self.item_type == 'potion':
            self.storage.health += 1
        
class ParticleEffectSprite(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.z = Z_LAYERS["fg"]

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

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
            self.image = pygame.transform.flip(self.image, flip_x=self.reverse["x"], flip_y=self.reverse["y"])

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

class Cloud(Sprite):
    def __init__(self, cloud_dir, cloud_speed, pos, surf, groups, z=Z_LAYERS['clouds']):
        super().__init__(pos, surf, groups)
        self.cloud_speed = cloud_speed
        self.cloud_dir = cloud_dir
        self.z = z
        self.rect.midbottom = pos

    def move(self, dt):
        self.rect.x += self.cloud_speed * dt * self.cloud_dir

    def update(self, dt):
        self.move(dt)
        if self.rect.right <= 0:
            self.kill()

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, level, storage, paths) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(pos[0] + TILE_SIZE / 2, pos[1] + TILE_SIZE / 2))
        self.z = Z_LAYERS['path']
        self.level = level
        self.storage = storage
        self.paths = paths
        self.grid_pos = (int(pos[0] / TILE_SIZE), int(pos[1] / TILE_SIZE))

    def can_move(self, direction):
        if direction in list(self.paths.keys()) and int(self.paths[direction][0][0]) <= self.storage.unlocked_level:
            return True

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames) -> None:
        super().__init__(groups)
        self.icon = True
        self.path = None
        self.direction = 0
        self.speed = 400

        self.frames, self.frame_index = frames, 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.z = Z_LAYERS['main']
        self.rect = self.image.get_frect(center=pos)

    def start_move(self, path):
        self.rect.center = path[0]
        self.path = path[1:]
        self.find_path()

    def find_path(self):
        if self.path:
            if self.rect.centerx == self.path[0][0]:
                self.direction = vector(0, 1 if self.path[0][1] > self.rect.centery else -1)
            else:
                self.direction = vector(1 if self.path[0][0] > self.rect.centerx else -1, 0)
        else:
            self.direction = vector()

    def point_collision(self):
        if self.direction.y == 1 and self.rect.centery >= self.path[0][1] or \
           self.direction.y == -1 and self.rect.centery <= self.path[0][1]:
            self.rect.centery = self.path[0][1]
            del self.path[0]
            self.find_path()

        if self.direction.x == 1 and self.rect.centerx >= self.path[0][0] or \
           self.direction.x == -1 and self.rect.centery <= self.path[0][0]:
            self.rect.centerx = self.path[0][0]
            del self.path[0]
            self.find_path()

    def get_state(self):
        if self.direction.x == 1:
            self.state = "right"
        elif self.direction.x == -1:
            self.state = 'left'
        elif self.direction.y == 1:
            self.state = "down"
        elif self.direction.y == -1:
            self.state = 'up'
        else: 
            self.state = 'idle'

    def animate(self, dt):
        self.frame_index += dt * ANIMATION_SPEED
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        
    def update(self, dt) -> None:

        if self.path:
            self.point_collision()
            self.rect.center += self.direction * self.speed * dt
            self.get_state()
            self.animate(dt)

class PathSprite(Sprite):
    def __init__(self, pos: tuple, surf: Surface, groups, level, z=Z_LAYERS['path']):
        super().__init__(pos, surf, groups, Z_LAYERS['path'])
        self.level = level
        self.z = z