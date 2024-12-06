# game_state.py

class GameState:
    _instance = None

    def __init__(self):
        if not GameState._instance:
            self.state = "menu"
            self.coins = 0  # Total de moedas acumuladas
            self.selected_character = "default"  # Personagem selecionado
            self.purchased_characters = ["default"]  # Personagens comprados
            GameState._instance = self

    @staticmethod
    def get_instance():
        if not GameState._instance:
            GameState()
        return GameState._instance
