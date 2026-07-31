from storage import Storage
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, load_pygame, pygame, sys, join
from level import level
from support import import_folder, import_sub_folders, import_image, import_folder_dict
from ui import UI
from overworld import Overworld

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption("Pirate")
		self.clock = pygame.time.Clock()
		self.import_assets()
		self.ui = UI(self.font, self.ui_frames)
		self.storage = Storage(self.ui)

		self.tmx_maps = {i: load_pygame(join('data', "levels", f"{i}.tmx")) for i in range(6)}
		

		self.tmx_overworld = load_pygame(join('data', 'overworld', 'overworld.tmx'))
		self.current_stage = level(self.tmx_maps[self.storage.current_level], self.level_frames, self.audio_files, self.storage, self.switch_stage)

		# self.current_stage = Overworld(self.tmx_overworld, self.storage, self.overworld_frames)

	def switch_stage(self, target, unlock=0):
		if target == 'level':
			self.current_stage = level(self.tmx_maps[self.storage.current_level], self.level_frames, self.audio_files ,self.storage, self.switch_stage)
			pass
		else:
			if unlock > 0:
				self.storage.unlocked_level = unlock
			else:
				self.storage.health -= 1
			self.current_stage = Overworld(self.tmx_overworld, self.storage, self.overworld_frames, self.switch_stage)
			
	def check_game_over(self):
		if self.storage.health <= 0:
			pygame.quit()
			sys.exit()

	def import_assets(self):
		self.level_frames = {
			'flag' : import_folder("graphics", "level", "flag"),
			'saw' : import_folder("graphics", "enemies", "saw", "animation"),
			'floor_spike' : import_folder("graphics", "enemies", "floor_spikes"),
			'palms' : import_sub_folders("graphics", "level", "palms"),
			'candle' : import_folder("graphics", "level", "candle"),
			'window' : import_folder("graphics", "level", "window"),
			'big_chain' : import_folder("graphics", "level", "big_chains"),
			'small_chain' : import_folder("graphics", "level", "small_chains"),
			'candle light' : import_folder("graphics", "level", "candle light"),
			'player' : import_sub_folders('graphics', "player"),
			'saw' : import_folder("graphics", "enemies", "saw", "animation"),
			'saw_chain' : import_image("graphics", "enemies", "saw", "saw_chain"),
			'helicopter' : import_folder("graphics", "level", "helicopter"),
			'boat' : import_folder("graphics", "objects", "boat"),
			'spike' : import_image('graphics', "enemies", "spike_ball", "Spiked ball"),
			'spike_chain' : import_image('graphics', "enemies", "spike_ball", "Spiked_chain"),
			'tooth' : import_folder('graphics', "enemies", "tooth", "run"),
			'shell' : import_sub_folders('graphics', "enemies", "shell"),
			'pearl' : import_image("graphics", "enemies", "bullets", "pearl"),
			'items' : import_sub_folders("graphics", "items"),
			'particle' : import_folder("graphics", "effects", "particle"),
			'water_top' : import_folder("graphics", "level", "water", "top"),
			'water_body' : import_image("graphics", "level", "water", "body"),
			'bg_tiles' : import_folder_dict("graphics", "level", "bg", 'tiles'),
			'small_clouds' : import_folder("graphics", "level", 'clouds', 'small'),
			'large_cloud' : import_image("graphics", 'level', 'clouds', 'large_cloud'),
		}	
		self.font = pygame.font.Font(join("graphics", "ui", "runescape_uf.ttf"), 32)
		self.ui_frames = {
			'heart' : import_folder('graphics', 'ui', 'heart'),
			"coin" : import_image("graphics", "ui", "coin"),
		}
		self.overworld_frames = {
			'palms' : import_folder('graphics', 'overworld', 'palm'),
			'water' : import_folder('graphics', 'overworld', 'water'),
			'path' : import_folder_dict('graphics', 'overworld', 'path'),
			'icon' : import_sub_folders('graphics', 'overworld', 'icon')
		}
		self.audio_files = {
			'coin' : pygame.mixer.Sound(join('audio', 'coin.wav')),
			'attack' : pygame.mixer.Sound(join('audio', 'attack.wav')),
			'damage' : pygame.mixer.Sound(join('audio', 'damage.wav')),
			'hit' : pygame.mixer.Sound(join('audio', 'hit.wav')),
			'jump' : pygame.mixer.Sound(join('audio', 'jump.wav')),
			'pearl' : pygame.mixer.Sound(join('audio', 'pearl.wav')),
		}
		
	def run(self):
		while True:
			dt = self.clock.tick_busy_loop() / 1000
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()   
					sys.exit()
			self.check_game_over()
						
			self.current_stage.run(dt)

			self.ui.update(dt)
			
			pygame.display.flip()

			

	

if __name__ == "__main__":
	Game().run()