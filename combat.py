import pygame
from combat_state import AttackingState, DefendingState, HealingState
from commands import AttackCommand, DefendCommand, HealCommand
from game_state import GameState
import os

class CombatSystem:
    def __init__(self, screen, player, enemy):
        self.screen = screen
        self.player = player
        self.enemy = enemy
        self.turn = "player"
        self.font = pygame.font.Font(None, 28)  
        
        self.options = ["Atacar", "Defender", "Curar", "Provocar", "Magia", "Carregar Ki"]
        self.selected = 0

        self.background = pygame.image.load(os.path.join('assets', 'images', 'combat_background.png')).convert()
        self.player_image = pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'images', f'{self.player.character_type}.gif')).convert_alpha(),
            (80, 80)  
        )
        self.enemy_image = pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'images', 'enemy1.gif')).convert_alpha(),
            (80, 80)  
        )

        
        try:
            self.attack_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'soco.mp3'))
            self.victory_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'victory.mp3'))
            self.game_over_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'derrota.mp3'))
            self.taunt_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'taunt.mp3'))
            self.magic_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'magic.mp3'))
            self.ki_charge_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'ki_charge.mp3'))
        except pygame.error as e:
            print(f"Erro ao carregar som: {e}")

    def battle(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))  
            
           
            self.screen.blit(self.player_image, (50, 300))  
            self.screen.blit(self.enemy_image, (500, 300))  
            
            self.display_health()
            self.display_options() 
            
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    GameState.get_instance().state = "exit"
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        self.player_action()
                        if self.enemy.health <= 0:
                            print("Você venceu o combate!")
                            self.victory_sound.play()  
                            running = False
                            break
                        self.turn = "enemy"

            if self.turn == "enemy":
                self.enemy_action()
                if self.player.health <= 0:
                    print("Você foi derrotado!")
                    self.game_over_sound.play()  
                    running = False
                self.turn = "player"

    def display_options(self):
       
        for idx, option in enumerate(self.options):
            color = (255, 255, 255) if idx != self.selected else (255, 0, 0)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (20, 400 + idx * 20))

    def display_health(self):
        player_health = self.font.render(f"Vida Jogador: {self.player.health}", True, (255, 255, 255))
        enemy_health = self.font.render(f"Vida Inimigo: {self.enemy.health}", True, (255, 255, 255))
        self.screen.blit(player_health, (20, 20))
        self.screen.blit(enemy_health, (500, 20))

    def player_action(self):
        command = None  

        if self.selected == 0:
            state = AttackingState()
            command = AttackCommand(self.player)
            state.action(self.player, self.enemy)
            self.attack_sound.play()
        elif self.selected == 1:
            state = DefendingState()
            command = DefendCommand(self.player)
            state.action(self.player)
        elif self.selected == 2:
            state = HealingState()
            command = HealCommand(self.player)
            state.action(self.player)
        elif self.selected == 3:  # Provocar
            print("Jogador usou Provocar!")
            self.taunt_sound.play()
        elif self.selected == 4:  # Magia
            print("Jogador usou Magia!")
            self.magic_sound.play()
            self.enemy.health -= 15  
        elif self.selected == 5: 
            print("Jogador carregou Ki!")
            self.ki_charge_sound.play()
            self.player.attack_power += 5  

        
        if command:
            command.execute()

    def enemy_action(self):
        import random
        action = random.choice(["attack", "defend", "heal"])
        if action == "attack":
            print("Inimigo Atacou!")
            self.enemy.attack(self.player)
            self.attack_sound.play()
        elif action == "defend":
            print("Inimigo Defendeu!")
            self.enemy.defend()
        elif action == "heal":
            print("Inimigo Curou!")
            self.enemy.heal()
