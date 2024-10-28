# observer.py

import pygame
from game_state import GameState

class Subject:
    def __init__(self):
        self._observers = []

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def attach(self, observer):
        self._observers.append(observer)

class Coin(pygame.sprite.Sprite, Subject):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        Subject.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 223, 0))  # Cor dourada para a moeda
        self.rect = self.image.get_rect()
        self.rect.center = position

    def collect(self):
        self.notify()
        self.kill()  # Remove a moeda do grupo de sprites

class PlayerObserver:
    def __init__(self, player):
        self.player = player

    def update(self, subject):
        if isinstance(subject, Coin):
            self.player.coins += 1
            GameState.get_instance().coins = self.player.coins  # Atualiza o GameState
            print("Moeda coletada! Total de moedas:", self.player.coins)
