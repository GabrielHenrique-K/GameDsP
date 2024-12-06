# character_select.py

import pygame
from game_state import GameState

class CharacterSelect:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.options = ["Personagem Azul", "Personagem Vermelho", "Personagem Verde", "Voltar"]
        self.characters = ["default", "v", "f"]
        self.selected = 0
        self.font = pygame.font.Font(None, 36)

    def display(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            for idx, option in enumerate(self.options):
                character = self.characters[idx] if idx < len(self.characters) else None
                if character and character not in self.game_state.purchased_characters:
                    option += " (Bloqueado)"
                color = (255, 255, 255)
                if idx == self.selected:
                    color = (255, 0, 0)
                text = self.font.render(option, True, color)
                self.screen.blit(text, (100, 100 + idx * 40))

                if idx < len(self.characters):
                    character_color = (0, 0, 255) if self.characters[idx] == "default" else \
                                      (255, 0, 0) if self.characters[idx] == "v" else \
                                      (0, 255, 0) if self.characters[idx] == "f" else (255, 255, 255)
                    pygame.draw.rect(self.screen, character_color, (50, 105 + idx * 40, 30, 30))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.game_state.state = "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected < len(self.characters):
                            character = self.characters[self.selected]
                            if character in self.game_state.purchased_characters:
                                self.game_state.selected_character = character
                                print(f"Personagem selecionado: {self.game_state.selected_character}")
                            else:
                                print("Personagem não comprado!")
                        running = False
                        self.game_state.state = "menu"
