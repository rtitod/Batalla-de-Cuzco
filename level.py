import math
import pygame
import sys

from harmless_npc import *
from vars import *
from collections import deque
from functools import lru_cache
from random import choices, randrange
from npc import *
from animated_sprite import *
from player import *
from weapon import Sling


class Level:
    def __init__(self, game):
        self.harmless_quantities = None
        self.npc_harmless_types = None
        self.history_image = None
        self.health_recovery_delay = None
        self.player_pos = None
        self.boss_max_rows = None
        self.boss_min_rows = None
        self.boss_max_cols = None
        self.boss_min_cols = None
        self.theme_sound = None
        self.player_pain_sound = None
        self.visited = None
        self.restricted_area = None
        self.sound_path = 'resources/sound/'
        self.graph = None
        self.npc_positions_object = None
        self.ways = None
        self.anim_sprite_path = None
        self.static_sprite_path = None
        self.npc_sprite_path = None
        self.map = None
        self.npc_list = None
        self.sprite_list = None
        self.textures = None
        self.objects_to_render = None
        self.ray_casting_result = None
        self.win_image = None
        self.game_over_image = None
        self.digits = None
        self.digit_images = None
        self.digit_size = None
        self.blood_screen = None
        self.sky_offset = None
        self.weapon = None
        self.boss_quantities = None
        self.quantities = None
        self.npc_boss_types = None
        self.npc_types = None
        self.sky_image = None
        self.wall_textures = None
        self.cols = None
        self.rows = None
        self.world_map = None
        self.mini_map = None
        self.player = None
        self.playerdeath = False

        self.screen = game.screen
        self.clock = game.clock
        self.delta_time = game.delta_time
        self.global_trigger = game.global_trigger
        self.global_event = game.global_event

        self.new_game()

    def override_player_vars(self):
        self.player_pos = 1.5, 5
        self.health_recovery_delay = 1000
    def override_vars(self):
        self.mini_map = mini_map
        self.npc_types = [ChancaSubversivo]
        self.npc_boss_types = [GeneralChanca]
        self.quantities = [8]
        self.boss_quantities = [1]
        self.npc_harmless_types = None
        self.harmless_quantities = [0]
        self.weapon = Sling(self)
        self.boss_min_cols = 1 / 9
        self.boss_max_cols = 4 / 9
        self.boss_min_rows = 7 / 9
        self.boss_max_rows = 9 / 9
        self.win_image = self.get_texture('resources/textures/win.png', RES)
        self.history_image = self.get_texture('resources/textures/history.png', RES)
        self.theme_sound = pygame.mixer.music.load(self.sound_path + 'theme.mp3')

    def new_game(self):
        print("Iniciando un nuevo juego")
        self.override_player_pos()
        self.player = Player(self)
        self.override_vars()
        self.world_map = {}
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.get_map()
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.wall_textures

        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/sprite_estatico/'
        self.anim_sprite_path = 'resources/sprites/sprites_animados/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions_object = {}
        # spawn npc
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.spawn_npc()
        self.spawn_harmless_npc()
        # sprite map
        self.add_candela()

        self.map = self.mini_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.get_graph()
        pygame.mixer.init()
        self.player_pain_sound = pygame.mixer.Sound(self.sound_path + 'player_pain.wav')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

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

    def update(self):
        self.player.update()
        self.update_raycasting()
        self.update_object()
        self.weapon.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.draw_Renderer()
        self.weapon.draw()
    def check_events(self):
        self.global_trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw_map(self):
        [pygame.draw.rect(self.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1
        ox, oy = self.player.pos
        x_map, y_map = self.player.map_pos

        ray_angle = self.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.world_map:
                    texture_hor = self.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.world_map:
                    texture_vert = self.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.player.angle - ray_angle)

            # proyeccion
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update_raycasting(self):
        self.ray_cast()
        self.get_objects_to_render()


    @lru_cache
    def get_path(self, start, goal):
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_nodes = graph[cur_node]

            for next_node in next_nodes:
                if next_node not in visited and next_node not in self.npc_positions_object:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def get_next_nodes(self, x, y):
        next_nodes = []
        for dx, dy in self.ways:
            new_x = x + dx
            new_y = y + dy
            if (new_x, new_y) not in self.world_map:
                next_nodes.append((new_x, new_y))
        return next_nodes

    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

    def draw_Renderer(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def win_Renderer(self):
        self.screen.blit(self.win_image, (0, 0))

    def history_Renderer(self):
        self.screen.blit(self.history_image, (0, 0))

    def game_over_Renderer(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        global i
        health = str(self.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage_Renderer(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pygame.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }

    def spawn_npc(self):
        all_npcs = []
        for npc_type, quantity in zip(self.npc_types, self.quantities):
            npcs_of_type = [npc_type for _ in range(quantity)]
            all_npcs.extend(npcs_of_type)
        for npc in all_npcs:
            pos = x, y = randrange(self.cols), randrange(self.rows)
            while (pos in self.world_map) or (pos in self.restricted_area):
                pos = x, y = randrange(self.cols), randrange(self.rows)
            self.add_npc(npc(self, pos=(x + 0.5, y + 0.5)))
        self.spawn_boss_npc()

    def spawn_boss_npc(self):
        all_npcs = []
        for npc_type, quantity in zip(self.npc_boss_types, self.boss_quantities):
            npcs_of_type = [npc_type for _ in range(quantity)]
            all_npcs.extend(npcs_of_type)
        for npc in all_npcs:
            pos = x, y = (randrange(int(self.boss_min_cols * self.cols), int(self.boss_max_cols * self.cols)),
                          randrange(int(self.boss_min_rows * self.rows), int(self.boss_max_rows * self.rows)))
            while (pos in self.world_map) or (pos in self.restricted_area):
                pos = x, y = (randrange(int(self.boss_min_cols * self.cols), int(self.boss_max_cols * self.cols)),
                              randrange(int(self.boss_min_rows * self.rows), int(self.boss_max_rows * self.rows)))
            self.add_npc(npc(self, pos=(x + 0.5, y + 0.5)))

    def spawn_harmless_npc(self):
        if self.npc_harmless_types is not None:
            all_npcs = []
            for npc_type, quantity in zip(self.npc_harmless_types, self.harmless_quantities):
                npcs_of_type = [npc_type for _ in range(quantity)]
                all_npcs.extend(npcs_of_type)
            for npc in all_npcs:
                pos = x, y = randrange(self.cols), randrange(self.rows)
                while (pos in self.world_map) or (pos in self.restricted_area):
                    pos = x, y = randrange(self.cols), randrange(self.rows)
                self.add_npc(npc(self, pos=(x + 0.5, y + 0.5)))

    def check_win(self):
        if not len(self.npc_positions_object):
            self.win_Renderer()
            pygame.display.flip()
            pygame.time.delay(2000)
            self.history_Renderer()
            pygame.display.flip()
            pygame.time.delay(6000)
            self.next_level()

    def next_level(self):
        self.new_game()

    def update_object(self):
        self.npc_positions_object = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        if self.playerdeath == False:
            self.check_win()
        else:
            self.playerdeath = False

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
