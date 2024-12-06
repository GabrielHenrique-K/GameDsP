# player.py

import pygame
from PIL import Image
from attack_strategy import FireAttack
from game_state import GameState
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, character_type='default'):
        super().__init__()
        self.character_type = character_type  
        self.load_gif_frames()  

        
        self.coins = GameState.get_instance().coins  
        self.health = 100
        self.attack_power = 10  
        self.is_defending = False
        self.attack_strategy = FireAttack()
        
        
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150  
        self.velocity_y = 0
        self.on_ground = True

        
        try:
            self.jump_sound = pygame.mixer.Sound('assets/sounds/dbz-teleport.mp3')
        except pygame.error as e:
            print(f"Erro ao carregar som de pulo: {e}")

    def load_gif_frames(self):
        """Carrega os frames de um GIF usando Pillow e converte para o formato do Pygame."""
        gif_path = os.path.join('assets', 'images', f'{self.character_type}.gif')
        
        try:
            pil_image = Image.open(gif_path)
        except IOError:
            print(f"Erro ao carregar GIF: {gif_path}")
            self.frames = [pygame.Surface((32, 32))]  
            return
        
        self.frames = []
        for frame in range(pil_image.n_frames):
            pil_image.seek(frame)
            frame_image = pil_image.convert("RGBA")
            mode = frame_image.mode
            size = frame_image.size
            data = frame_image.tobytes()
            pygame_image = pygame.image.fromstring(data, size, mode).convert_alpha()
            self.frames.append(pygame.transform.scale(pygame_image, (64, 64)))  

    def update(self):
        """Atualiza o frame atual para simular animação."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def move(self, dx, dy):
        """Movimenta o jogador e aplica a gravidade."""
        self.rect.x += dx
        self.rect.y += dy

    def jump(self):
        """Faz o jogador pular."""
        if self.on_ground:
            self.velocity_y = -15
            self.on_ground = False
            if hasattr(self, 'jump_sound'):
                self.jump_sound.play()

    def apply_gravity(self, ground_group):
        """Aplica a gravidade ao jogador e verifica a colisão com o chão."""
        self.velocity_y += 1  # Gravidade
        self.rect.y += self.velocity_y
        
        
        collision_list = pygame.sprite.spritecollide(self, ground_group, False)
        if collision_list:
            self.rect.bottom = collision_list[0].rect.top
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def attack(self, target):
        """Executa o ataque no alvo."""
        self.attack_strategy.attack(target)
        print("Ataque realizado!")

    def defend(self):
        """Defende-se contra o próximo ataque."""
        self.is_defending = True
        print("Você está Defendendo!")

    def heal(self):
        """Recupera parte da vida."""
        self.health += 10
        if self.health > 100:
            self.health = 100
        print("Você recuperou 10 de vida. Vida atual:", self.health)
