import pygame
from game_state import GameState
from menu import MainMenu
from character_factory import CharacterFactory
from observer import Coin, PlayerObserver
from combat import CombatSystem
from shop import Shop
from ground import Ground
from character_select import CharacterSelect
from enemy import Enemy
import os

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((150, 75, 0))  # Marrom para as plataformas
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Jogo Estilo Mario com Combate por Turnos")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    game_state = GameState.get_instance()
    running = True

    # Carregar imagem de fundo
    background_image = pygame.image.load(os.path.join('assets', 'images', 'background.png')).convert()
    background_image = pygame.transform.scale(background_image, (1280, 480))  # Fundo maior para rolar

    player = CharacterFactory.create_character("player", x=100, y=300, character_type=game_state.selected_character)
    player_observer = PlayerObserver(player)
    
    all_sprites = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    ground_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()  # Grupo de plataformas

    all_sprites.add(player)

    # Criar o chão
    ground = Ground(0, 400, 640, 80)
    all_sprites.add(ground)
    ground_group.add(ground)

    # Criar plataformas
    platforms = [
        Platform(200, 300, 100, 20),
        Platform(400, 250, 100, 20),
        Platform(600, 200, 100, 20),
        Platform(800, 300, 100, 20)
    ]
    for platform in platforms:
        platform_group.add(platform)
        all_sprites.add(platform)

    # Criar moedas
    for i in range(5):
        coin = Coin((100 + i * 60, 350))
        coins.add(coin)
        all_sprites.add(coin)
        coin.attach(player_observer)

    # Criar inimigos e colocar em algumas plataformas
    enemy_positions = [(300, 350), (500, 300), (700, 250), (900, 200)]
    for pos in enemy_positions:
        enemy = Enemy(*pos)
        enemies.add(enemy)
        all_sprites.add(enemy)

    # Variável para rastrear o deslocamento da câmera (scroll)
    camera_offset = 0

    while running:
        if game_state.state == "menu":
            menu = MainMenu(screen)
            menu.display()
            if game_state.state == "exit":
                running = False
        elif game_state.state == "playing":
            # Loop de jogo
            playing = True
            while playing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_state.state = "exit"
                        running = False
                        playing = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and player.on_ground:
                            player.velocity_y = -15  # Ajuste no pulo
                            player.on_ground = False  # Indica que o jogador está no ar
                        elif event.key == pygame.K_a:
                            if enemies:
                                current_enemy = enemies.sprites()[0]  # Ataca o primeiro inimigo na lista
                                player.attack(current_enemy)
                        elif event.key == pygame.K_d:
                            player.defend()  # Defender

                # Movimentação do jogador
                keys_pressed = pygame.key.get_pressed()
                dx = 0
                if keys_pressed[pygame.K_LEFT]:
                    dx = -5
                elif keys_pressed[pygame.K_RIGHT]:
                    dx = 5

                # Move o jogador
                player.rect.x += dx

                # Aplicar gravidade e ajustar colisão com plataformas e chão
                player.velocity_y += 1  # Gravidade
                player.rect.y += player.velocity_y
                
                # Verifica a colisão com o chão
                if pygame.sprite.spritecollide(player, ground_group, False):
                    player.rect.y = 400 - player.rect.height  # Posição em cima do chão
                    player.velocity_y = 0
                    player.on_ground = True
                else:
                    player.on_ground = False

                # Verifica a colisão com plataformas
                if pygame.sprite.spritecollide(player, platform_group, False):
                    player.velocity_y = 0  # Interrompe o movimento vertical ao colidir com plataformas

                # Atualizar rolagem do fundo e impedir desaparecimento do jogador
                if player.rect.x > 320 and dx > 0 and camera_offset > -640:
                    camera_offset -= dx
                    player.rect.x = 320

                # Atualiza todas as sprites
                all_sprites.update()

                # Verificar colisão com moedas
                coins_hit_list = pygame.sprite.spritecollide(player, coins, False)
                for coin in coins_hit_list:
                    coin.collect()
                    coins.remove(coin)
                    all_sprites.remove(coin)

                # Verificar colisão com inimigos
                enemy_hit_list = pygame.sprite.spritecollide(player, enemies, False)
                if enemy_hit_list:
                    game_state.state = "combat"
                    current_enemy = enemy_hit_list[0]
                    combat_system = CombatSystem(screen, player, current_enemy)
                    combat_system.battle()
                    if current_enemy.health <= 0:
                        enemies.remove(current_enemy)
                        all_sprites.remove(current_enemy)
                    if player.health <= 0:
                        game_state.state = "defeat"
                        playing = False
                    elif len(enemies) == 0:
                        game_state.state = "victory"
                        playing = False

                # Renderizar o jogo
                screen.fill((135, 206, 235))  # Fundo azul claro
                screen.blit(background_image, (camera_offset, 0))
                for entity in all_sprites:
                    screen.blit(entity.image, (entity.rect.x + camera_offset, entity.rect.y))

                # Exibir contador de moedas
                coin_text = font.render(f"Moedas: {player.coins}", True, (255, 255, 255))
                screen.blit(coin_text, (10, 10))

                pygame.display.flip()
                clock.tick(60)
        
        elif game_state.state == "defeat":
            # Exibir mensagem de derrota
            screen.fill((0, 0, 0))
            defeat_text = font.render("Você foi Derrotado!", True, (255, 0, 0))
            screen.blit(defeat_text, (200, 200))
            pygame.display.flip()
            pygame.time.wait(2000)
            game_state.state = "menu"
        elif game_state.state == "victory":
            # Exibir mensagem de vitória
            screen.fill((0, 0, 0))
            victory_text = font.render("Você Venceu Todos os Inimigos!", True, (0, 255, 0))
            screen.blit(victory_text, (150, 200))
            pygame.display.flip()
            pygame.time.wait(2000)
            game_state.state = "menu"
        elif game_state.state == "shop":
            shop = Shop(screen, game_state)
            shop.display()
            if game_state.state == "exit":
                running = False
        elif game_state.state == "select_character":
            character_select = CharacterSelect(screen, game_state)
            character_select.display()
            if game_state.state == "exit":
                running = False
        elif game_state.state == "exit":
            pygame.quit()
            break

if __name__ == "__main__":
    main()
