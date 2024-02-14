from abc import ABC, abstractmethod
from random import randint

class Player(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def play_one_action(self, grid):
        pass

class HumanPlayer(Player):
    def play_one_action(self, grid):
        return int(input())

class AIPlayer(Player):
    def play_one_action(self, grid):
        return randint(1,7)

