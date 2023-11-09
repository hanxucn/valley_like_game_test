import pygame

from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Trees
from pytmx.util_pygame import load_pygame
from support import import_folder


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

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

        # fence
        for x, y, surf in tmx_data.get_layer_by_name("Fence").tiles():
            Generic(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=surf, group=[self.all_sprites, self.collision_sprites],
                z=LAYERS["main"]
            )

        # water
        water_frames = import_folder("./graphics/water")
        for x, y, surf in tmx_data.get_layer_by_name("Water").tiles():
            Water(pos=(x * TILE_SIZE, y * TILE_SIZE), frames=water_frames, group=self.all_sprites)

        # flower
        for obj in tmx_data.get_layer_by_name("Decoration"):
            WildFlower(pos=(obj.x, obj.y), surf=obj.image, group=[self.all_sprites, self.collision_sprites])

        # trees
        for obj in tmx_data.get_layer_by_name("Trees"):
            Trees(pos=(obj.x, obj.y), surf=obj.image, group=[self.all_sprites, self.collision_sprites], name=obj.name)

        self.player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), self.all_sprites, self.collision_sprites)
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
            # 按照 y 坐标排序，保证了 y 坐标大的 sprite 在上面,实现物体前后关系
            for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
                if sprite.z == layer:
                    # 所有 sprites 向着 player 移动的反方向移动，保证了 camera 的位置不变
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
