import pygame
from settings import *

class Upgrade:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attributes_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.height = self.display_surface.get_size()[1] * 0.6
        self.width = self.display_surface.get_size()[0] // 7
        self.create_items()

        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_number - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 0:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_RETURN]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        self.item_list = []
        
        for index, item in enumerate(range(self.attribute_number)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // (self.attribute_number + 1)
            left = (item * increment) + (increment - self.width) // 0.25

            top = self.display_surface.get_size()[1] * 0.2

            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            name = self.attributes_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)


class Item():
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        title_surface = self.font.render(name, False, color)
        title_rect = title_surface.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

        cost_surface = self.font.render(f'cost: {int(cost)}', False, color)
        cost_rect = cost_surface.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))

        surface.blit(title_surface, title_rect)
        surface.blit(cost_surface, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        color = UPGRADE_BG_COLOR_ACTIVE if selected else BAR_COLOR

        left = self.rect.center
        ratio = (value / max_value[self.index]) * (bottom[1] - top[1])
        rectangle = pygame.Rect(left[0], top[1], 10, (bottom-top)[1])
        progressbar_rect = pygame.Rect(left[0], (bottom[1]-ratio), 10, ratio)

        pygame.draw.rect(surface, color, rectangle, border_radius=10)
        pygame.draw.rect(surface, EXPERIENCE_BACKGROUND, progressbar_rect, border_radius=10)
        pygame.draw.rect(surface, UI_BORDER_COLOR, rectangle, 2, border_radius=10)

    def trigger(self, player):
            upgrade_attribute =list(player.stats.keys())[self.index]

            if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
                player.exp -= player.upgrade_cost[upgrade_attribute]
                player.stats[upgrade_attribute] *= 1.2
                player.upgrade_cost[upgrade_attribute] *= 1.4
            
            if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
                player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_ACTIVE, self.rect, border_radius=10)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4, border_radius=10)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect, border_radius=10)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4, border_radius=10)

        self.display_names(surface, name, cost, self.index == selection_num)
        self.display_bar(surface, value, max_value, self.index == selection_num)
