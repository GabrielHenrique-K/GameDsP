# character_factory.py

from player import Player
from enemy import Enemy

class CharacterFactory:
    @staticmethod
    def create_character(character_role, **kwargs):
        if character_role == "player":
            return Player(**kwargs)
        elif character_role == "enemy":
            return Enemy(**kwargs)
