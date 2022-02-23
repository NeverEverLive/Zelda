import pygame
from csv import reader
from os import walk


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []
    sorted_surface_list = []
    for _, __, images in walk(path):
        for image in images:
            full_path = '/'.join([path, image])
            surface_list.append(full_path)

        surface_list.sort()
        
        for surface in surface_list:
            image_surface = pygame.image.load(surface).convert_alpha()
            sorted_surface_list.append(image_surface)

    return sorted_surface_list

# import_csv_layout('../map/map_FloorBlocks.csv')
# import_folder('../texture/grass')