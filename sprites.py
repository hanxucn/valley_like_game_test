import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, z=LAYERS["main"]):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)


class Water(Generic):
    def __init__(self, pos, frames, group):
        self.frames = frames
        self.frame_index = 0

        # sprite setup
        super().__init__(pos=pos, surf=self.frames[self.frame_index], group=group, z=LAYERS["water"])

        self.frame_rate = 0.5
        self.animation_timer = 0

    def animate(self, dt):
        self.animation_timer += 2 * dt
        if self.animation_timer >= self.frame_rate:
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[self.frame_index]
            self.animation_timer = 0

    def update(self, dt):
        self.animate(dt)


class WildFlower(Generic):
    def __init__(self, pos, surf, group):
        super().__init__(pos=pos, surf=surf, group=group)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)


class Trees(Generic):
    def __init__(self, pos, surf, group, name):
        super().__init__(pos=pos, surf=surf, group=group)
