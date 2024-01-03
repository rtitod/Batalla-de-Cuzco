from level_1 import *
from level_2 import *
from level_3 import *
from level_4 import *


class game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(RES)
        pygame.event.set_grab(True)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.global_event, 40)

if __name__ == '__main__':
    game = game()
    start = Level_4(game)
    start.run()
