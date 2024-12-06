# main_menu.py

import pygame
import os
from game_state import GameState

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Iniciar Jogo", "Comprar Personagens", "Selecionar Personagem", "Sair"]
        self.selected = 0
        self.font = pygame.font.Font(None, 36)
        
        
        try:
            self.background = pygame.image.load(os.path.join('assets', 'images', 'backmenu.png')).convert()
            self.background = pygame.transform.scale(self.background, (640, 480))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo: {e}")
            self.background = None

    def display(self):
        game_state = GameState.get_instance()
        running = True
        while running:
            
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 0))  

            
            for idx, option in enumerate(self.options):
                color = (255, 255, 255) if idx != self.selected else (255, 0, 0)
                text = self.font.render(option, True, color)
                self.screen.blit(text, (100, 100 + idx * 40))

           
            coins_text = self.font.render(f"Moedas: {game_state.coins}", True, (255, 255, 0))
            self.screen.blit(coins_text, (10, 10))
            pygame.display.flip()

            # Lidar com eventos do menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_state.state = "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        
                        if self.selected == 0:
                            game_state.state = "playing"
                            running = False
                        elif self.selected == 1:
                            game_state.state = "shop"
                            running = False
                        elif self.selected == 2:
                            game_state.state = "select_character"
                            running = False
                        elif self.selected == 3:
                            game_state.state = "exit"
                            running = False
