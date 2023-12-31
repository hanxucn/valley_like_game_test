import pygame


class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func
        self.active = False
        self.start_time = 0

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current = pygame.time.get_ticks()
        if current - self.start_time >= self.duration:
            self.deactivate()
            if self.func:
                self.func()
