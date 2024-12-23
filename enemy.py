# enemy.py

import pygame
import os
import random
from attack_strategy import WaterAttack

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
  
        enemy_images = [
            os.path.join('assets', 'images', 'enemy1.gif'),
            os.path.join('assets', 'images', 'enemy2.gif')
        ]
        selected_image_path = random.choice(enemy_images)

    
        try:
            self.image = pygame.image.load(selected_image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))  
        except pygame.error as e:
            print(f"Erro ao carregar imagem do inimigo: {e}")
            self.image = pygame.Surface((64, 64))  
            self.image.fill((255, 0, 0))  

      
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        
        self.health = 50
        self.attack_strategy = WaterAttack()
        self.is_defending = False

    def update(self):
        """Atualize o estado do inimigo, se necessário."""
        pass  

    def attack(self, target):
        """Executa o ataque no alvo."""
        self.attack_strategy.attack(target)

    def defend(self):
        """Defende-se contra o próximo ataque."""
        self.is_defending = True
        print("Inimigo está Defendendo!")

    def heal(self):
        """Recupera parte da vida."""
        self.health += 5
        if self.health > 50:
            self.health = 50
        print("Inimigo recuperou 5 de vida. Vida atual do inimigo:", self.health)
