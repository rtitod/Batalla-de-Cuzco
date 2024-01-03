from animated_sprite import *

# hereda de AnimatedSprite
class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/sling/0.png', scale=0.4, animation_time=20):
        # Llamada al constructor de la clase base
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)

        # Escalado de imágenes y configuración de posición
        scaled_images = []
        for img in self.images:
            scaled_img = pygame.transform.smoothscale(img,
                                                      (self.image.get_width() * scale, self.image.get_height() * scale))
            scaled_images.append(scaled_img)
        self.images = deque(scaled_images)

        # Posición inicial del arma
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())

        # Configuración de la recarga
        self.reloading = False

        # Configuración de la previa
        self.previous = False

        # Número de imágenes y contador de fotogramas
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.num_images_prev = 17

        # Daño del arma
        self.damage = 50

    def animate_shot(self):
        # Animación del disparo
        if self.previous == True:
            if self.animation_trigger == True:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images_prev + 1:
                    self.reloading = True
                    self.game.player.shot = True
                    self.previous = False
        else:
            if self.reloading == True:
                self.game.player.shot = False
                if self.animation_trigger == True:
                    self.images.rotate(-1)
                    self.image = self.images[self.num_images_prev]
                    self.frame_counter += 1
                    if self.frame_counter == self.num_images:
                        self.reloading = False
                        self.frame_counter = 0

    def draw(self):
        # Dibuja el arma en la pantalla
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        # Actualiza el estado del arma
        self.check_animation_time()
        self.animate_shot()

class Sling(Weapon):
    def __init__(self, game, path='resources/sprites/weapon/sling/0.png', scale=0.4, animation_time=20):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.num_images_prev = 17
        self.game.player.gun_sound = pygame.mixer.Sound(self.game.sound_path + 'sling.wav')
        self.damage = 50

class Shotgun(Weapon):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=100):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.num_images_prev = 0
        self.game.player.gun_sound = pygame.mixer.Sound(self.game.sound_path + 'shotgun.wav')
        self.damage = 100

