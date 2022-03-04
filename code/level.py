from sqlite3 import paramstyle
import pygame
from random import choice, randint

from settings import TILESIZE
from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI
from enemy import Enemy
from utils import import_csv_layout, import_folder
from debug import debug
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from death import Death

class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.player_is_dead = False

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.create_map()

        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        self.main_sound = pygame.mixer.Sound('../audio/main.ogg')
        self.main_sound.set_volume(0.5)
        self.main_sound.play(loops=-1)

    def create_map(self) -> None:
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'objects': import_csv_layout('../map/map_Objects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
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
                            Tile(
                                (x,y), 
                                [
                                    self.visible_sprites, 
                                    self.obstacle_sprites, 
                                    self.attackable_sprites
                                ], 
                                'grass', 
                                random_grass_image
                            )
                        if style == 'objects':
                            surface = graphics['objects'][int(column)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)
                        if style == 'entities':
                            if column == '394':
                                self.player = Player(
                                    (x, y), 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_attack,
                                    self.create_magic,
                                    self.player_dead
                                )
                            else:
                                if column == '390': monster_name = 'bamboo'
                                elif column == '391': monster_name = 'spirit'
                                elif column == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp
                                )        

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            position = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(position - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
 
    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, position, particle_type):
        self.animation_player.create_particles(particle_type, position, self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def player_dead(self):
        self.main_sound.stop()
        death_sound = pygame.mixer.Sound('../audio/player_death.wav')
        death_sound.set_volume(0.5)
        death_sound.play(loops=-1)
        self.player_is_dead = True
        self.game_paused = True

    def run(self) -> None:
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        
        if self.player_is_dead:
            Death().display()
        elif self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

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

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
