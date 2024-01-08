import math
from random import randint, random
from animated_sprite import *
from vars import *


class Harmless_NPC(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/crow/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        # Llama al constructor de la clase base
        super().__init__(game, path, pos, scale, shift, animation_time)

        # Configuración de imágenes para diferentes estados del NPC
        self.idle_images = self.get_images(self.path + '/idle')
        self.walk_images = self.get_images(self.path + '/walk')

        # Propiedades del NPC
        self.speed = 0.03
        self.size = 20
        self.alive = False
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False

    def update(self):
        # Actualiza el NPC en cada ciclo del juego
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        # self.draw_ray_cast()

    def check_wall(self, x, y):
        # Verifica si hay una pared en la posición dada
        if (x, y) not in self.game.world_map:
            return x, y

    def check_wall_collision(self, dx, dy):
        # Verifica la colisión con las paredes después del movimiento
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        # Lógica de movimiento del NPC
        next_pos = self.game.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        # pygame.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
        if next_pos not in self.game.npc_positions_object:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def run_logic(self):
        # Lógica principal del NPC
        if self.alive == False:
            self.ray_cast_value = self.ray_cast_player_npc()

            if self.ray_cast_value:
                self.player_search_trigger = True

                if self.dist < 0:
                    self.animate(self.walk_images)
                else:
                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)

    @property
    def map_pos(self):
        # Propiedad que devuelve la posición del NPC en el mapa
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):
        # Realiza un lanzamiento de rayos para determinar si el jugador está en la línea de visión
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        if sin_a > 0:
            y_hor = y_map + 1
            dy = 1
        else:
            y_hor = y_map - 1e-6
            dy = -1

        if sin_a != 0:
            depth_hor = (y_hor - oy) / sin_a
        else:
            # Manejar el caso cuando sin_a es cero, por ejemplo, asignando un valor predeterminado .
            depth_hor = 0

        x_hor = ox + depth_hor * cos_a

        if sin_a != 0:
            delta_depth = dy / sin_a
        else:
            # Manejar el caso cuando sin_a es cero, por ejemplo, asignando un valor predeterminado .
            delta_depth = 0

        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        if cos_a > 0:
            x_vert = x_map + 1
            dx = 1
        else:
            x_vert = x_map - 1e-6
            dx = -1

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_ray_cast(self):
        # Dibuja el rayo de visión del NPC
        pygame.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pygame.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                             (100 * self.x, 100 * self.y), 2)

class Stars(Harmless_NPC):
    def __init__(self, game, path='resources/sprites/npc/stars/0.png', pos=(10.5, 6.5),
                 scale=0.01, shift=0.27, animation_time=150):
        # Llamada al constructor de la clase base
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.speed = 0.040

