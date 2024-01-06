from level import *
from weapon import *


class Level_4(Level):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

    def override_player_pos(self):
        self.player_pos = 1.5, 1.5
        self.health_recovery_delay = 700

    def override_vars(self):
        self.mini_map = mini_map4
        self.npc_types = [SoldadoEspanolBallesta, SoldadoEspanolHacha]
        self.npc_boss_types = [GeneralEspanol3]
        self.quantities = [6, 14]
        self.boss_quantities = [1]
        self.weapon = Shotgun(self)
        self.boss_min_cols = 4 / 5
        self.boss_max_cols = 5 / 5
        self.boss_min_rows = 4 / 5
        self.boss_max_rows = 5 / 5

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5_3.png'),
        }

    def next_level(self):
        from level_1 import Level_1
        nxt_level = Level_1(self.game)
        nxt_level.run()
