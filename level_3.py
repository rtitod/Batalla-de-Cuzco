from level import *
from weapon import *


class Level_3(Level):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

    def override_player_pos(self):
        self.player_pos = 2, 2
        self.health_recovery_delay = 700

    def override_vars(self):
        self.mini_map = mini_map3
        self.npc_types = [SoldadoEspanolBallesta]
        self.npc_boss_types = [GeneralEspanol2]
        self.quantities = [18]
        self.boss_quantities = [1]
        self.weapon = Shotgun(self)
        self.boss_min_cols = 1 / 18
        self.boss_max_cols = 7 / 18
        self.boss_min_rows = 11 / 12
        self.boss_max_rows = 12 / 12

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5_2.png'),
        }

    def next_level(self):
        from level_4 import Level_4
        nxt_level = Level_4(self.game)
        nxt_level.run()
