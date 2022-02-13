import pygame

from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups) -> None:
        super().__init__(groups)
        self.image = pygame.image.load('../texture/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)
