import os
import re
from collections import deque
import pygame
from sprite_object import *

# hereda de Spriteobject
class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/sprites_animados/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        # Llamada al constructor de la clase base
        super().__init__(game, path, pos, scale, shift)

        # Configuración de la animación
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pygame.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        # Actualización de la animación
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        # Animación de las imágenes
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        # Comprobación del tiempo de animación
        self.animation_trigger = False
        time_now = pygame.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        # Obtención de las imágenes para la animación
        images = deque()
        for file_name in sorted(os.listdir(path), key=self.natural_sort_key):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pygame.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images

    def natural_sort_key(self, s):
        # Clave de ordenación natural para ordenar archivos numéricamente
        result = []
        for text in re.split('([0-9]+)', s):
            if text.isdigit():
                result.append(int(text))
            else:
                result.append(text.lower())
        return result
