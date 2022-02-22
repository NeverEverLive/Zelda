import pygame
from random import choice

from settings import TILESIZE, WORLD_MAP
from tile import Tile
from player import Player
from utils import import_csv_layout, import_folder
from debug import debug


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self) -> None:
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'objects': import_csv_layout('../map/map_Objects.csv')
        }
        graphics = {
            'grass': import_folder('../texture/grass'),
            'objects': import_folder('../texture/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for column_index, column in enumerate(row):
                    if column != '-1':
                        x = column_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'objects':
                            surface = graphics['objects'][int(column)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)
                            
        self.player = Player((2000,1430), [self.visible_sprites], self.obstacle_sprites)

    def run(self) -> None:
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load('../texture/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft= (0,0))

    def custom_draw(self, player) -> None:
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_possition = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_possition)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_position)
