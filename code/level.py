from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite
from player import Player
from groups import AllSprites

class level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pg.display.get_surface()
        
        self.all_sprites = AllSprites()
        self.collison_sprites = pg.sprite.Group()
        self.semi_collidables = pg.sprite.Group()
        self.damage_sprites = pg.sprite.Group()

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        # // tiles
        for layer in ["BG", "Terrian", "FG", "Platforms"]:
            for x, y, image in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrian' : groups.append(self.collison_sprites)
                if layer == 'Platforms' : groups.append(self.semi_collidables)
                match layer:
                    case "BG" : z = Z_LAYERS["bg tiles"]
                    case "FG" : z= Z_LAYERS['bg tiles']
                    case _ : z = Z_LAYERS["main"]
                Sprite((x * TILE_SIZE, y * TILE_SIZE), image, groups, z)

        # // bg details
        for obj in tmx_map.get_layer_by_name('BG details'):
            if obj.name == "static":
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, z=Z_LAYERS["bg tiles"])
            else:
                AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites, Z_LAYERS['bg tiles'])
                if obj.name == "candle":
                    AnimatedSprite((obj.x, obj.y) + vector(-20, -20), level_frames['candle light'], self.all_sprites)
        
        # // objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "player":
                self.player = Player(
                    pos=(obj.x, obj.y), 
                    groups=self.all_sprites, 
                    collision_sprites=self.collison_sprites,
                    semi_collidables=self.semi_collidables,
                    frames=level_frames['player'])
            else:
                if obj.name in ("barrel", "crate"):
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collison_sprites))
                else:
                    frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
                    if obj.name == "floor_spike" and obj.properties["inverted"]:
                        flipped_frames = [pg.transform.flip(frame, False, True) for frame in frames]
                        frames = flipped_frames
                    AnimatedSprite((obj.x, obj.y), frames, self.all_sprites)
                    
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == "spike":
               pass  
            else:
                frames = level_frames[obj.name]
                groups = (self.all_sprites, self.semi_collidables) if obj.properties["platform"] else (self.all_sprites, self.damage_sprites)
                if obj.width > obj.height: # horizontal
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else:
                    move_dir = 'y' # vertical
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties['speed']
                MovingSprite(obj.name, frames, groups, start_pos, end_pos, move_dir, speed, obj.properties["flip"])
                

                if obj.name == "saw":
                    if move_dir == "x":
                        y = start_pos[1] - level_frames["saw_chain"].get_height() / 2
                        left, right = int(start_pos[0]), int(end_pos[0])
                        for x in range(left, right, 20):
                            Sprite((x, y), level_frames["saw_chain"], self.all_sprites, z=Z_LAYERS["bg details"])
                    else:
                        x = start_pos[0] - level_frames["saw_chain"].get_width() / 2
                        top, bottom = int(start_pos[1]), int(end_pos[1])
                        for y in range(top, bottom, 20):
                            Sprite((x, y), level_frames["saw_chain"], self.all_sprites, z=Z_LAYERS["bg details"])
                        


    def run(self, dt):
        self.display_surface.fill((0, 0, 0))
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center)
        for sprite in self.semi_collidables:
            if str(sprite) == "boat":
                print(sprite.reverse)