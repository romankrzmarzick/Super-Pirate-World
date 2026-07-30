from settings import *
from random import choice
from time_track import Timer

class Tooth(pg.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft=pos)
        self.z = Z_LAYERS["main"]
        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]

        self.speed = 100
        self.detect_rects = {"edge" : False, "wall" : False}

        self.hit_timer = Timer(415)
       
    def reverse(self):
        if not self.hit_timer.active:
            self.direction *= -1
            self.hit_timer.activate()

    def contact_check(self):
        wall_rect = pg.Rect(self.rect.center - vector(-1, 0), (self.rect.width + 2, 1))
        if self.direction == -1: floor_rect = pg.FRect((self.rect.bottomleft), (-1, 1))
        else: floor_rect = pg.FRect((self.rect.bottomright), (100, 100))
        
        self.detect_rects["edge"] = False if floor_rect.collidelist(self.collision_rects) >= 0 else True
        self.detect_rects["wall"] = True if wall_rect.collidelist(self.collision_rects) >= 0 else False

    def reverse_check(self):
        if self.detect_rects["edge"] or self.detect_rects["wall"]: self.direction *= -1 


    def update(self, dt):
        self.hit_timer.update()

        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pg.transform.flip(self.image, flip_x=True, flip_y=False) if self.direction == -1 else self.image

        self.contact_check()
        self.reverse_check()

        # move
        self.rect.x += self.direction * self.speed * dt
        # reverse direction

class Shell(pg.sprite.Sprite):
    def __init__(self, pos, frames, groups, reverse, player, create_pearl):
        super().__init__(groups)
        
        if reverse:
            self.frames = {}
            for key, surfs in frames.items():
                self.frames[key] = [pg.transform.flip(surf, True, False) for surf in surfs]  
            self.bullet_direction = -1

        else:
            self.frames = frames
            self.bullet_direction = 1

        self.frame_index = 0
        self.state = "idle"
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS["main"]
        self.player = player

        self.shoot_timer = Timer(2500)
        self.has_fired = False

        self.create_pearl = create_pearl

    def state_management(self):
        player_pos, shell_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center) 
        player_near = shell_pos.distance_squared_to(player_pos) < 50000
        player_front = shell_pos.x < player_pos.x if self.bullet_direction > 0 else shell_pos.x > player_pos.x
        player_level = abs(shell_pos.y - player_pos.y) < 30

        if player_near and player_front and player_level and not self.shoot_timer.active:
            self.state = "fire"
            self.frame_index = 0
            self.shoot_timer.activate()


    def update(self, dt):
        self.shoot_timer.update()
        self.state_management()

        #animation / attack
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]

            # fire
            if self.state == "fire" and int(self.frame_index) == 3 and not self.has_fired:
                self.create_pearl(self.rect.center, self.bullet_direction)
                self.has_fired = True

        else: 
            self.frame_index = 0 
            if self.state == "fire":
                self.state = "idle"
                self.has_fired = False

class Pearl(pg.sprite.Sprite):
    def __init__(self, pos, groups, surf, direction, speed):
        super().__init__(groups)
        self.image = surf
        self.direction = direction
        self.rect = self.image.get_frect(center=pos + vector(50 * direction, 0))
        self.speed = speed
        self.z = Z_LAYERS["main"]

        self.timers = {"lifetime" : Timer(4000, self.kill_sprite, autostart=True), "reverse_timer" : Timer(415)}
        
        self.pearl = True

        

    def kill_sprite(self):
        self.kill()

    def reverse(self):
        if not self.timers["reverse_timer"].active:
            self.direction *= -1
            self.timers["reverse_timer"].activate()

    def move(self, dt):
        self.rect.x += self.speed * dt * self.direction

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.timer_update()
        self.move(dt)
       
       