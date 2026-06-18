from settings import * 
from level import level
from support import *



class Game:
	def __init__(self):
		pg.init()
		self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pg.display.set_caption("Pirate")
		self.clock = pg.time.Clock()
		self.import_assets()
		
		self.tmx_maps = {0: load_pg(join('data', "levels", "omni.tmx"))}
		self.current_stage = level(self.tmx_maps[0], self.level_frames)
		

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
			'pearl' : import_image("graphics", "enemies", "bullets", "pearl")
		}	

		
	def run(self):
		while True:
			dt = self.clock.tick_busy_loop() / 1000
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()   
					sys.exit()
			
			self.current_stage.run(dt)
			
			
			pg.display.flip()

	

if __name__ == "__main__":
	Game().run()