# game_state.py

class GameState:
    _instance = None

    def __init__(self):
        if not GameState._instance:
            self.state = "menu"
            self.coins = 0  
            self.selected_character = "default"  
            self.purchased_characters = ["default"]  
            GameState._instance = self

    @staticmethod
    def get_instance():
        if not GameState._instance:
            GameState()
        return GameState._instance
