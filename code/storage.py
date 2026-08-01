class Storage:
    def __init__(self, ui):
        self.ui = ui
        self._coins: int = 0
        self._health: int = 30
        self.ui.create_hearts(self._health)

        self.unlocked_level = 0
        self.current_level = 0

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = value
        self.ui.create_hearts(self._health)

    @property
    def coins(self) -> int:
        return self._coins

    @coins.setter
    def coins(self, value: int):
        self._coins = value
        if self._coins >= 100:
            self._coins -= 100
            self.health += 1
        

        self.ui.show_coins(self._coins)


    