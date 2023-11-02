
import sys
import pygame

from level import Level
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("xuxu land")
        self.running = True
        self.level = Level()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit()

            dt = self.clock.tick(60) / 1000.0
            self.level.run(dt)
            pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
