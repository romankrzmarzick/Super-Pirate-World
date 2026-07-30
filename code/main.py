from storage import Storage
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, load_pg, pg, sys, join
from level import level
from support import import_folder, import_sub_folders, import_image, import_folder_dict
from debug import debug
from ui import UI

class Game:
	def __init__(self):
		pg.init()
		self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pg.display.set_caption("Pirate")
		self.clock = pg.time.Clock()
		self.import_assets()
		self.ui = UI(self.font, self.ui_frames)
		self.storage = Storage(self.ui)

		self.tmx_maps = {0: load_pg(join('data', "levels", "omni.tmx"))}
		self.current_stage = level(self.tmx_maps[0], self.level_frames, self.storage)
		

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
		self.font = pg.font.Font(join("graphics", "ui", "runescape_uf.ttf"), 32)
		self.ui_frames = {
			'heart' : import_folder('graphics', 'ui', 'heart'),
			"coin" : import_image("graphics", "ui", "coin"),
		}
		
	def run(self):
		while True:
			dt = self.clock.tick_busy_loop() / 1000
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()   
					sys.exit()
			
			self.current_stage.run(dt)

			self.ui.update(dt)
			
			pg.display.flip()

			

	

if __name__ == "__main__":
	Game().run()