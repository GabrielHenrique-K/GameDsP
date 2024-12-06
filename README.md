---

# GameDsP

## Descrição

**GameDsP** é um jogo baseado em Python que combina elementos de combate, escolha de personagens e mecânicas de RPG. O projeto utiliza diversas bibliotecas para manipulação de sprites, sons e interação do jogador, com um foco em oferecer uma experiência imersiva.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
GameDsP/
├── assets/                 # Recursos como imagens e sons
│   ├── images/             # Sprites e fundos
│   ├── sounds/             # Efeitos sonoros e músicas
├── .git/                   # Diretório de controle de versão
├── __pycache__/            # Arquivos compilados em Python
├── main.py                 # Arquivo principal para execução do jogo
├── combat_state.py         # Gerenciamento do estado de combate
├── character_factory.py    # Criação e gerenciamento de personagens
├── commands.py             # Implementação de comandos
├── character_select.py     # Tela de seleção de personagens
├── spritesheet.py          # Manipulação de spritesheets
├── ground.py               # Configuração do cenário
├── player.py               # Lógica e comportamento do jogador
├── combat.py               # Mecânicas de combate
├── observer.py             # Padrão de observador para eventos
├── attack_strategy.py      # Estratégias de ataque
├── game_state.py           # Gerenciamento do estado global do jogo
├── menu.py                 # Interface de menus
├── enemy.py                # Comportamento de inimigos
├── shop.py                 # Implementação de um sistema de loja
```

## Pré-requisitos

Para executar o projeto, você precisa ter o seguinte instalado:

- Python 3.10 ou superior
- Bibliotecas listadas no arquivo `requirements.txt` (se aplicável)

## Como Executar

1. Clone o repositório:
   ```bash
   git clone (https://github.com/GabrielHenrique-K/GameDsP.git)
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd GameDsP
   ```
3. Execute o jogo:
   ```bash
   python main.py
   ```

## Recursos

- **Gráficos**: Sprites de desenhos.
- **Áudio**: Efeitos sonoros.
- **Jogabilidade**: Combate RPG e Arcade.
