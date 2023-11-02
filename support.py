from os import walk

import pygame


def import_folder(path):
    surface_list = []
    for _, _, image_files in walk(path):
        for image in image_files:
            full_path = f"{path}/{image}"
            image_surface = pygame.image.load(full_path).convert_alpha()
            original_width, original_height = image_surface.get_size()

            new_width = original_width
            new_height = original_height

            # 使用 pygame.transform.scale 进行缩放
            scaled_image = pygame.transform.scale(image_surface, (new_width, new_height))
            surface_list.append(scaled_image)
    return surface_list
