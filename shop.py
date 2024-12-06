# shop.py

import pygame
from game_state import GameState

class Shop:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.options = ["Personagem Vermelho - 5 moedas", "Personagem Verde - 10 moedas", "Voltar"]
        self.characters = ["v", "f"]
        self.prices = [5, 10]
        self.selected = 0
        self.font = pygame.font.Font(None, 36)

    def display(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            for idx, option in enumerate(self.options):
                color = (255, 255, 255)
                if idx == self.selected:
                    color = (255, 0, 0)
                text = self.font.render(option, True, color)
                self.screen.blit(text, (50, 100 + idx * 40))

            coins_text = self.font.render(f"Moedas: {self.game_state.coins}", True, (255, 255, 0))
            self.screen.blit(coins_text, (10, 10))
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
                            price = self.prices[self.selected]
                            if character in self.game_state.purchased_characters:
                                print(f"Você já possui o {self.options[self.selected]}!")
                            elif self.game_state.coins >= price:
                                self.game_state.coins -= price
                                self.game_state.purchased_characters.append(character)
                                print(f"Você comprou o {self.options[self.selected]}!")
                            else:
                                print("Moedas insuficientes!")
                        else:
                            self.game_state.state = "menu"
                            running = False
