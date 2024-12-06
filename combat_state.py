# combat_state.py

class CombatState:
    def action(self, context, target=None):
        pass

class AttackingState(CombatState):
    def action(self, context, target):
        print("Você escolheu Atacar!")
        context.attack(target)

class DefendingState(CombatState):
    def action(self, context, target=None):
        print("Você escolheu Defender!")
        context.defend()

class HealingState(CombatState):
    def action(self, context, target=None):
        print("Você escolheu Curar!")
        context.heal()
