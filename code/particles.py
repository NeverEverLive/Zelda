import pygame
from utils import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'flame': import_folder('../texture/particles/flame/frames'),
            'aura': import_folder('../texture/particles/aura'),
            'heal': import_folder('../texture/particles/heal/frames'),
        
            'claw': import_folder('../texture/particles/claw'),
            'slash': import_folder('../texture/particles/slash'),
            'sparkle': import_folder('../texture/particles/sparkle'),
            'leaf_attack': import_folder('../texture/particles/leaf_attack'),
            'thunder': import_folder('../texture/particles/thunder'),

            'squid': import_folder('../texture/particles/smoke_orange'),
            'raccoon': import_folder('../texture/particles/raccoon'),
            'spirit': import_folder('../texture/particles/nova'),
            'bamboo': import_folder('../texture/particles/bamboo'),
            
            'leaf': (
                import_folder('../texture/particles/leaf1'),
                import_folder('../texture/particles/leaf2'),
                import_folder('../texture/particles/leaf3'),
                import_folder('../texture/particles/leaf4'),
                import_folder('../texture/particles/leaf5'),
                import_folder('../texture/particles/leaf6'),
                self.reflect_images(import_folder('../texture/particles/leaf1')),
                self.reflect_images(import_folder('../texture/particles/leaf2')),
                self.reflect_images(import_folder('../texture/particles/leaf3')),
                self.reflect_images(import_folder('../texture/particles/leaf4')),
                self.reflect_images(import_folder('../texture/particles/leaf5')),
                self.reflect_images(import_folder('../texture/particles/leaf6'))

                )
        }

    def reflect_images(self, frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        
        return new_frames

    def create_grass_particles(self, position, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(position, animation_frames, groups)

    def create_particles(self, animation_type, position, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(position, animation_frames, groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = position)
        

    def animation(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames): self.kill()
        else: self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animation()