import pygame
import os

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        ground_texture = pygame.image.load(os.path.join('assets', 'images', 'ground.png')).convert_alpha()
        ground_texture = pygame.transform.scale(ground_texture, (width, height))
        self.image.blit(ground_texture, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y