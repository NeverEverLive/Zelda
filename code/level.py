import pygame

from settings import TILESIZE, WORLD_MAP
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self) -> None:

        self.diplay_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for colimn_index, column in enumerate(row):
                x = colimn_index * TILESIZE
                y = row_index * TILESIZE
                if column == 'x':
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
                if column == 'p':
                    self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)

    def run(self) -> None:
        self.visible_sprites.draw(self.diplay_surface)
        self.visible_sprites.update()
        debug(self.player.direction)