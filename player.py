import pygame

from settings import *
from support import import_folder
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)
        # self.animations = {}
        self.animations = {}
        self.import_assets()
        self.status = "down_idle"
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS["main"]

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        self.idle_animation_delay = 0.8
        self.move_animation_delay = 0.2
        self.last_update = 0

        # collision
        self.hitbox = self.rect.copy().inflate(-126, -70)
        self.collision_sprites = collision_sprites

        self.timer = {
            "tool use": Timer(350, self.use_tool),
            "tool switch": Timer(200),
            "seed use": Timer(350, self.use_seed),
            "seed switch": Timer(200),
        }
        self.tools = ["hoe", "axe", "water"]
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seed
        self.seeds = ["corn", "tomato"]
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

    def use_tool(self):
        pass

    def use_seed(self):
        pass

    def import_assets(self):
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": [],
            "up_hoe": [], "down_hoe": [], "left_hoe": [], "right_hoe": [],
            "up_axe": [], "down_axe": [], "left_axe": [], "right_axe": [],
            "up_water": [], "down_water": [], "left_water": [], "right_water": [],
        }
        for animation in self.animations.keys():
            full_path = f"./graphics/character/{animation}"
            self.animations[animation] = import_folder(full_path)

    def animation(self, dt):
        self.last_update += dt
        if "idle" in self.status:
            animation_delay = self.idle_animation_delay
        else:
            animation_delay = self.move_animation_delay
        if self.last_update >= animation_delay:
            self.frame_index += 1
            self.last_update = 0
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timer["tool use"].active:
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            # tool use
            if keys[pygame.K_SPACE]:
                self.timer["tool use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # tool switch
            if keys[pygame.K_q] and not self.timer["tool switch"].active:
                self.timer["tool switch"].activate()
                self.tool_index += 1
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]
                # self.timer["tool use"].deactivate()

            # seed use
            if keys[pygame.K_LCTRL]:
                self.timer["seed use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                print(f"use seed {self.selected_seed}")

            # seed switch
            if keys[pygame.K_e] and not self.timer["seed switch"].active:
                self.timer["seed switch"].activate()
                self.seed_index += 1
                self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
                self.selected_seed = self.seeds[self.seed_index]
                print(f"switch seed to {self.selected_seed}")

        # else:
        #     if keys[pygame.K_SPACE]:
        #         self.update_timers()

    def update_timers(self):
        for timer in self.timer.values():
            timer.update()

    def get_status(self):

        # idle status which is not moving
        if self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0] + "_idle"

        # tool use
        if self.timer["tool use"].active:
            self.status = self.status.split("_")[0] + "_" + self.selected_tool

        # if self.timer["tool switch"].active:
        #     self.status = self.status.split("_")[0] + "_" + self.selected_tool

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, "hitbox"):
                if self.hitbox.colliderect(sprite.hitbox):
                    if direction == "horizontal":
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        elif self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    elif direction == "vertical":
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        elif self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animation(dt)
