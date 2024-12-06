import random

class GameState:
    """
    Singleton Pattern: Garante que apenas uma instância do estado do jogo exista.
    Gerencia informações globais, como o nível atual e se o jogo está rodando.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            cls._instance.level = 1
            cls._instance.is_running = True
        return cls._instance

class CharacterFactory:
    """
    Factory Pattern: Responsável por criar instâncias de personagens (jogador ou inimigo).
    Permite criar diferentes tipos de personagens sem expor a lógica de criação.
    """
    @staticmethod
    def create_character(name, role):
        stats = {
            "Warrior": {"health": 120, "attack": 25},
            "Mage": {"health": 80, "attack": 35},
            "Rogue": {"health": 100, "attack": 20},
            "Enemy": {"health": 100, "attack": 15},
        }
        return Character(name, stats[role]["health"], stats[role]["attack"], role)

class GameObserver:
    """
    Observer Pattern: Notifica os jogadores sobre eventos importantes no jogo.
    Responsável por exibir mensagens informativas para o jogador.
    """
    def notify(self, message):
        print(f"\n[NOTIFICAÇÃO]: {message}")

class Character:
    """
    Representa um personagem do jogo com atributos básicos como vida e ataque.
    Pode ser usado para o jogador ou inimigos.
    """
    def __init__(self, name, health, attack_power, role):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.role = role

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount

class AttackStrategy:
    """
    Strategy Pattern: Define diferentes estratégias para o comportamento do inimigo.
    Permite que o inimigo altere entre estratégias agressivas, defensivas e balanceadas.
    """
    def execute(self, enemy, player):
        raise NotImplementedError()

class AggressiveStrategy(AttackStrategy):
    def execute(self, enemy, player):
        damage = random.randint(10, enemy.attack_power)
        player.take_damage(damage)
        return f"{enemy.name} atacou agressivamente e causou {damage} de dano!"

class DefensiveStrategy(AttackStrategy):
    def execute(self, enemy, player):
        healing = random.randint(5, 15)
        enemy.heal(healing)
        return f"{enemy.name} se curou em {healing} pontos!"

class BalancedStrategy(AttackStrategy):
    def execute(self, enemy, player):
        if random.choice([True, False]):
            return AggressiveStrategy().execute(enemy, player)
        else:
            return DefensiveStrategy().execute(enemy, player)

class Command:
    """
    Command Pattern: Encapsula ações do jogador em comandos reutilizáveis.
    Permite que ações como ataque, cura e ataque especial sejam executadas de forma independente.
    """
    def execute(self):
        raise NotImplementedError()

class AttackCommand(Command):
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def execute(self):
        damage = random.randint(10, self.player.attack_power)
        self.enemy.take_damage(damage)
        return f"Você atacou e causou {damage} de dano em {self.enemy.name}!"

class HealCommand(Command):
    def __init__(self, player):
        self.player = player

    def execute(self):
        healing = random.randint(10, 20)
        self.player.heal(healing)
        return f"Você se curou em {healing} pontos de vida!"

class SpecialCommand(Command):
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def execute(self):
        if random.random() > 0.3:
            damage = self.player.attack_power * 2
            self.enemy.take_damage(damage)
            return f"Você usou um ataque especial e causou {damage} de dano!"
        else:
            return "Seu ataque especial falhou!"

def next_level(game_state, observer, player):
    """
    Avança o jogo para o próximo nível, criando um novo inimigo mais forte.
    """
    game_state.level += 1
    enemy = CharacterFactory.create_character(f"Inimigo Nível {game_state.level}", "Enemy")
    observer.notify(f"Você avançou para o Nível {game_state.level}!")
    return enemy

def main():
    observer = GameObserver()
    game_state = GameState()

    print("Escolha sua classe:")
    print("1. Guerreiro (Warrior)")
    print("2. Mago (Mage)")
    print("3. Ladino (Rogue)")
    role_choice = input("> ")

    roles = {"1": "Warrior", "2": "Mage", "3": "Rogue"}
    role = roles.get(role_choice, "Warrior")
    player = CharacterFactory.create_character("Jogador", role)

    enemy = CharacterFactory.create_character("Inimigo Inicial", "Enemy")
    strategies = [AggressiveStrategy(), DefensiveStrategy(), BalancedStrategy()]

    observer.notify("O jogo começou!")

    while game_state.is_running:
        print(f"\nSua vida: {player.health} | Vida do inimigo: {enemy.health}")
        print("Escolha sua ação:")
        print("1. Atacar")
        print("2. Curar-se")
        print("3. Usar ataque especial")
        choice = input("> ")

        if choice == "1":
            command = AttackCommand(player, enemy)
        elif choice == "2":
            command = HealCommand(player)
        elif choice == "3":
            command = SpecialCommand(player, enemy)
        else:
            print("Comando inválido.")
            continue

        result = command.execute()
        observer.notify(result)

        if not enemy.is_alive():
            observer.notify(f"Você derrotou {enemy.name}!")
            enemy = next_level(game_state, observer, player)
            continue

        strategy = random.choice(strategies)
        result = strategy.execute(enemy, player)
        observer.notify(result)

        if not player.is_alive():
            observer.notify("Você perdeu!")
            game_state.is_running = False

if __name__ == "__main__":
    main()
