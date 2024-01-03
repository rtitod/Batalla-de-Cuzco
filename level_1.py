from level import *
from level_2 import Level_2
from weapon import *


class Level_1(Level):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

    def override_player_pos(self):
        self.player_pos = 2, 2
        self.health_recovery_delay = 1200

    def override_vars(self):
        self.mini_map = mini_map
        self.npc_types = [ChancaSubversivo]
        self.npc_boss_types = [GeneralChanca]
        self.quantities = [8]
        self.boss_quantities = [1]
        self.weapon = Sling(self)
        self.boss_min_cols = 1 / 9
        self.boss_max_cols = 4 / 9
        self.boss_min_rows = 7 / 9
        self.boss_max_rows = 9 / 9

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }

    def next_level(self):
        nxt_level = Level_2(self.game)
        nxt_level.run()
