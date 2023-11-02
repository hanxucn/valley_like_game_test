import pygame

from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame("./data/map.tmx")

        # house
        for layer_name in ["HouseFloor", "HouseFurnitureBottom"]:
            for x, y, surf in tmx_data.get_layer_by_name(layer_name).tiles():
                Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surf, group=self.all_sprites, z=LAYERS["house bottom"])

        for layer_name in ["HouseWalls", "HouseFurnitureTop"]:
            for x, y, surf in tmx_data.get_layer_by_name(layer_name).tiles():
                Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surf, group=self.all_sprites, z=LAYERS["main"])

        self.player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), self.all_sprites)
        Generic(
            pos=(0, 0),
            surf=pygame.image.load("./graphics/world/ground.png").convert_alpha(),
            group=self.all_sprites,
            z=LAYERS["ground"],
        )

    def run(self, dt):
        self.display_surface.fill("black")
        # self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    # 所有 sprites 向着 player 移动的反方向移动，保证了 camera 的位置不变
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)