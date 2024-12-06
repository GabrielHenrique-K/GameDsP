# commands.py

class Command:
    def execute(self):
        pass

class AttackCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        
        pass

class DefendCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        pass

class HealCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        pass
