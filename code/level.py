import pygame

from settings import TILESIZE, WORLD_MAP
from tile import Tile
from player import Player
from debug import debug


class Level:
    def __init__(self) -> None:

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self) -> None:
        for row_index, row in enumerate(WORLD_MAP):
            for colimn_index, column in enumerate(row):
                x = colimn_index * TILESIZE
                y = row_index * TILESIZE
                if column == 'x':
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
                if column == 'p':
                    self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)

    def run(self) -> None:
        # self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player) -> None:

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):

            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_position)
