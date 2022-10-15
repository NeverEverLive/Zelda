import pygame

from settings import *
from weapon import Weapon
from entity import Entity
from utils import import_folder

class Player(Entity):
    def __init__(self, position, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, player_dead) -> None:
        super().__init__(groups)
        self.image = pygame.image.load('../texture/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])

        self.import_player_assets()
        self.status = 'down'
        self.player_dead = player_dead

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_duration = 200
        self.attack_time = None
        
        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.switch_duration_cooldown = 200
        self.weapon_switch_time = None

        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.weapon_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        
        self.stats = {
            'health': 100,
            'energy': 60,
            'attack': 10,
            'magic': 4,
            'speed': 6
        }
        self.max_stats = {
            'health': 300,
            'energy': 140,
            'attack': 20,
            'magic': 10,
            'speed': 10
        }
        self.upgrade_cost = {
            'health': 100,
            'energy': 100,
            'attack': 100,
            'magic': 100,
            'speed': 100
            
        }
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 0
        self.speed = self.stats['speed']

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.3)

    def input(self) -> None:
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
        
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        # attack input
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()
            self.weapon_attack_sound.play()
            
        if keys[pygame.K_q] and self.can_switch_weapon:
            self.weapon_index += 1

            if self.weapon_index == len(list(weapon_data.keys())):
                self.weapon_index = 0

            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            self.weapon = list(weapon_data.keys())[self.weapon_index]

        # magic input
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            style = list(magic_data.keys())[self.magic_index]
            strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
            cost = list(magic_data.values())[self.magic_index]['cost']
            self.create_magic(style, strength, cost)

        if keys[pygame.K_e] and self.can_switch_magic:
            self.magic_index += 1

            if self.magic_index == len(list(magic_data.keys())):
                self.magic_index = 0

            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()
            self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status += '_idle'

            if self.attacking:
                self.direction.x = 0
                self.direction.y = 0
                if not 'attack' in self.status:
                    if 'idle' in self.status:
                        self.status = self.status.replace('_idle', '_attack')
                    else:
                        self.status += '_attack'
            else:
                if '_attack' in self.status:
                    self.status = self.status.replace('_attack', '')
        
    def import_player_assets(self):
        character_path = '../texture/player'
        surface_list = []
        self.animation = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'up_attack': [],
            'down_attack': [],
            'left_attack': [],
            'right_attack': [],
            'up_idle': [],
            'down_idle': [],
            'left_idle': [],
            'right_idle': []
        }

        for animation in self.animation.keys():
            full_path = '/'.join([character_path, animation])
            self.animation[animation] = import_folder(full_path)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time <= self.attack_duration:
                self.direction = pygame.math.Vector2()
            else:
                self.destroy_attack()
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animation[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self) -> float:
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self) -> None:
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]
        
    def energy_recovery(self):
        if self.energy < self.stats['energy']: self.energy += 0.01 * self.stats['magic']
        else: self.energy = self.stats['energy']

    def check_death(self):
        if self.health <= 0:
            self.health = 0
            self.player_dead()

    def update(self) -> None:
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.energy_recovery()
        self.check_death()
        self.move(self.stats['speed'])
