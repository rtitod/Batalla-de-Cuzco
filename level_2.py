from level import *
from weapon import *


class Level_2(Level):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

    def override_player_pos(self):
        self.player_pos = 2, 2
        self.health_recovery_delay = 1000

    def override_vars(self):
        self.mini_map = mini_map2
        self.npc_types = [SoldadoEspanolHacha, SoldadoEspanolBallesta]
        self.npc_boss_types = [GeneralEspanol1]
        self.quantities = [10, 5]
        self.boss_quantities = [2]
        self.weapon = Sling(self)
        self.boss_min_cols = 1 / 18
        self.boss_max_cols = 6 / 18
        self.boss_min_rows = 7 / 9
        self.boss_max_rows = 9 / 9
        self.win_image = self.get_texture('resources/textures/win.png', RES)
        self.history_image = self.get_texture('resources/textures/history2.png', RES)
        self.theme_sound = pygame.mixer.music.load(self.sound_path + 'theme.mp3')

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5_1.png'),
        }

    def add_candela(self):
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(11.5, 3.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(1.5, 1.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(1.5, 7.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(5.5, 3.25)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(5.5, 4.75)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(7.5, 2.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(7.5, 5.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(14.5, 1.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(14.5, 4.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 5.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 7.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 12.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 20.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'red_light/0.png', pos=(10.5, 20.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 14.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 18.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(14.5, 24.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(14.5, 30.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(1.5, 30.5)))
        self.add_sprite(AnimatedSprite(self, path=self.anim_sprite_path + 'green_light/0.png', pos=(1.5, 24.5)))

    def next_level(self):
        from level_3 import Level_3
        nxt_level = Level_3(self.game)
        nxt_level.run()
