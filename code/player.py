from settings import * 
from time_track import Timer
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semi_collidables, frames, storage, player_audio):
        # // setup
        super().__init__(groups)
        self.z = Z_LAYERS["main"]
        self.storage = storage

        # // image
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]

        # // rect
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox_rect = self.rect.inflate((-76, -36))
        self.old_rect = self.hitbox_rect.copy()
        
        # // movement
        self.dir = vector()
        self.speed = 250
        self.gravity = 1300
        self.jump_height = 800
        self.jump = False
        self.attacking = False
        
        # // collision
        self.collision_sprites = collision_sprites
        self.semi_collidables = semi_collidables
        self.on_surface = {"floor" : False, "left" : False, "right" : False}
        self.platform = None

        # // timer
        self.timers = {
            'wall jump': Timer(400),
            'wall slide block' : Timer(250),
            'platform skip' : Timer(100),
            'attack_cooldown' : Timer(600),
            'hit' : Timer(400),
        } 

        # audio 
        self.attack_sound = player_audio['attack']
        self.jump_sound = player_audio['jump']
        self.damage_sound = player_audio['damage']

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()
        
        if not self.timers["wall jump"].active:
            if keys[pygame.K_RIGHT]:
                input_vector.x += 1
                self.facing_right = True
            if keys[pygame.K_LEFT]:
                input_vector.x -= 1
                self.facing_right = False
            self.dir.x = input_vector.normalize().x if input_vector else 0  
        
        if keys[pygame.K_SPACE]:
            self.attack()

        if keys[pygame.K_UP]:
            self.jump = True
        
        if keys[pygame.K_DOWN]:
            self.timers["platform skip"].activate()

    def attack(self):
        if not self.timers['attack_cooldown'].active:
            self.attacking = True
            self.frame_index = 0
            self.timers["attack_cooldown"].activate()
            self.attack_sound.play()

    def move(self, dt):
        self.hitbox_rect.x += self.dir.x * self.speed * dt
        
        self.collision("x")
        self.semi_collision('x')

        # // y-movement
        if not self.on_surface["floor"] and any((self.on_surface["left"], self.on_surface["right"])) and not self.timers["wall slide block"].active and self.dir.y > 0 :
            self.dir.y = 0
            self.hitbox_rect.y += self.gravity / 10 * dt
        
        else:
            self.dir.y += self.gravity / 2 * dt 
            self.hitbox_rect.y += self.dir.y * dt
            self.dir.y += self.gravity / 2 * dt
        
        # // jump
        if self.jump:
            if self.on_surface["floor"]:
                self.timers["wall slide block"].activate()
                self.dir.y = -self.jump_height
                self.jump_sound.play()
                # // jump stick adjustment
                self.hitbox_rect.bottom -= 1
            # // wall jump
            elif not self.timers["wall slide block"].active:
                if any((self.on_surface["right"], self.on_surface["left"])):
                    self.timers['wall jump'].activate()
                    self.dir.y = -self.jump_height
                    self.dir.x = 1 if self.on_surface["left"] else -1
            self.jump = False
            
        self.collision("y")
        self.semi_collision("y")

        self.rect.center = self.hitbox_rect.center

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def platform_move(self, dt):
        if self.platform:
            self.hitbox_rect.topleft += self.platform.dir * self.platform.speed * dt

    def check_contact(self):
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        right_rect = pygame.Rect((self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4)), (2, self.hitbox_rect.height / 2))
        left_rect = pygame.Rect((self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4)), (2, self.hitbox_rect.height / 2))
        
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rects = [sprite.rect for sprite in self.semi_collidables]

        # // collisions
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semi_collide_rects) >= 0  and self.dir.y >= 0 else False
        self.on_surface["right"] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface["left"] = True if left_rect.collidelist(collide_rects) >= 0 else False

        # // semi_collidables check
        self.platform = None
        collision_sprites = self.collision_sprites.sprites() + self.semi_collidables.sprites()


        for sprite in [sprite for sprite in collision_sprites if hasattr(sprite, "moving")]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite

    def semi_collision(self, dir):
        for sprite in self.semi_collidables:
            if self.hitbox_rect.colliderect(sprite.rect):
                if dir == "y":
                    if not self.timers["platform skip"].active:
                        if self.hitbox_rect.bottom >= sprite.rect.top and (self.old_rect.bottom) <= sprite.old_rect.top + 1:
                            if self.dir.y >= 0: self.dir.y = 0
                            self.hitbox_rect.bottom = sprite.rect.top
    
    def collision(self, axis):
        for sprite in self.collision_sprites:
            if self.hitbox_rect.colliderect(sprite.rect):
                # // x-axis
                if axis == "x":
                    # right-side self.rect
                    if self.hitbox_rect.right >= sprite.rect.left and (self.old_rect.right) <= sprite.old_rect.left + 1:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.hitbox_rect.left <= sprite.rect.right and (self.old_rect.left) >= sprite.old_rect.right - 1:
                        self.hitbox_rect.left = sprite.rect.right
                    
                else:
                    if self.hitbox_rect.bottom >= sprite.rect.top and (self.old_rect.bottom) <= sprite.old_rect.top + 1:
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.dir.y = 0
                    if self.hitbox_rect.top <= sprite.rect.bottom and (self.old_rect.top) >= sprite.old_rect.bottom - 1:
                        self.hitbox_rect.top = sprite.rect.bottom
                        self.dir.y = 0
                        if hasattr(sprite, "moving"): 
                            self.hitbox_rect.top += 6       

    def get_state(self):
        if self.on_surface['floor']:
            if self.attacking:
                self.state = "attack"
            else:
                self.state = 'idle' if self.dir.x == 0 else 'run'
        else:
            if self.attacking:
                self.state = "air_attack"
            else:
                if any((self.on_surface["right"], self.on_surface['left'])):
                    self.state = 'wall'
                else:
                    self.state = 'jump' if self.dir.y < 0 else 'fall'

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.state == 'attack' and self.frame_index >= len(self.frames[self.state]):
            self.state = "idle"
        self.image = self.frames[self.state][(int(self.frame_index) % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
    
        if self.attacking and self.frame_index > len(self.frames[self.state]):
            self.attacking = False

    def get_damage(self):
        if not self.timers['hit'].active:
            self.storage.health -= 1
            self.timers['hit'].activate()
            self.damage_sound.play()

    def flicker(self):
        if self.timers["hit"].active and sin(pygame.time.get_ticks() * 100) >= 0:
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey((0,0,0))
            self.image = white_surf


    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.platform_move(dt)
        self.check_contact()    
        self.get_state()
        self.animate(dt)

        self.flicker()