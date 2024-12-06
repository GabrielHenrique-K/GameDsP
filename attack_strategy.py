# attack_strategy.py

class AttackStrategy:
    def attack(self, target):
        pass

class FireAttack(AttackStrategy):
    def attack(self, target):
        damage = 10
        print("Ataque de Fogo causa", damage, "de dano!")
        if target.is_defending:
            damage = int(damage / 2)
            print("O dano foi reduzido pela metade devido à defesa!")
            target.is_defending = False
        target.health -= damage

class WaterAttack(AttackStrategy):
    def attack(self, target):
        damage = 8
        print("Ataque de Água causa", damage, "de dano!")
        if target.is_defending:
            damage = int(damage / 2)
            print("O dano foi reduzido pela metade devido à defesa!")
            target.is_defending = False
        target.health -= damage
