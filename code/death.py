from curses.textpad import rectangle
import pygame
from settings import *


class Death():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.width = 600
        self.height = 400
        self.font = pygame.font.Font(UI_FONT, 38)

    def display_title(self):
        color = 'red'

        width, height = self.display_surface.get_size()

        title_surface = self.font.render("you are dead", False, color)
        title_rect = title_surface.get_rect(center = pygame.math.Vector2(width//2, height//2))

        self.display_surface.blit(title_surface, title_rect)

    def display_death_menu(self):
        left = (self.display_surface.get_size()[0]-self.width)//2
        top = (self.display_surface.get_size()[1]-self.height)//2
        print(left)
        print(top)
        rectangle = pygame.Rect(left, top, self.width, self.height)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, rectangle, border_radius=10)

    def display(self):
        self.display_death_menu()
        self.display_title()