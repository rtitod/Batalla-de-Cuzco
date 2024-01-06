import pygame

from vars import *

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = self.game.player_pos
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = self.game.health_recovery_delay
        self.time_prev = pygame.time.get_ticks()
        # corrección de movimiento diagonal
        self.diag_move_corr = 1 / math.sqrt(2)
        self.gun_sound = None

    def recover_health(self):
        # Recupera la salud del jugador si ha pasado el tiempo de recuperación
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        # Verifica si ha pasado el tiempo necesario para recuperar la salud
        time_now = pygame.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        # Comprueba si la salud del jugador es menor que 1 y muestra la pantalla de Game Over
        if self.health < 1:
            self.game.game_over_Renderer()
            pygame.display.flip()
            pygame.time.delay(1500)
            self.game.playerdeath = True
            self.game.new_game()

    def get_damage(self, damage):
        # Reduce la salud del jugador y muestra los efectos de daño
        self.health -= damage
        self.game.player_damage_Renderer()
        self.game.player_pain_sound.play()
        self.check_game_over()

    # disparando contra el adversario
    def single_fire_event(self, event):
        # Maneja el evento de disparo del jugador
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 1 and self.shot == False
                    and self.game.weapon.reloading == False
                    and self.game.weapon.previous == False):
                self.gun_sound.play()
                self.game.weapon.previous = True

    def movement(self):
        # Gestiona el movimiento del jugador
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()
        num_key_pressed = -1
        if keys[pygame.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pygame.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pygame.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos
        if keys[pygame.K_SPACE]:
            self.health = PLAYER_MAX_HEALTH

        # corrección de movimiento diagonal
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy)

        # if keys[pygame.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pygame.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    def check_wall(self, x, y):
        # Verifica si hay una pared en la posición especificada
        return (x, y) not in self.game.world_map

    def check_wall_collision(self, dx, dy):
        # Verifica la colisión con la pared y ajusta la posición del jugador
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        # Dibuja la posición y la orientación del jugador en la pantalla
        pygame.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        # Controla la orientación del jugador con el ratón
        mx, my = pygame.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        # Actualiza el estado del jugador en cada fotograma
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
