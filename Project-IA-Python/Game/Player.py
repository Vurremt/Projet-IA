from abc import ABC, abstractmethod
from numpy import ravel, sum, cumsum, searchsorted
from random import uniform, randint

class Player(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def play_one_action(self, grid):
        pass

class HumanPlayer(Player):
    def play_one_action(self, grid):
        return int(input())

class RandomPlayer(Player):
    def play_one_action(self, grid):
        return randint(1, 7)

class AIPlayer(Player):
    def __init__(self, name, network):
        super().__init__(name)
        self.network = network

    def play_one_action(self, grid):
        input = ravel(grid)
        self.network.add_state(0, input)

        results = self.network.feedforward(input)
        cumulative_proba = cumsum(results)

        rand = uniform(0, 1)
        action = searchsorted(cumulative_proba, rand)
        return action + 1  # +1 for being between 1 and 7

    def play_one_action_random(self, grid):
        input = ravel(grid)
        self.network.add_state(0, input)

        return randint(1, 7)

class AIPlayerLabyrinth(Player):
    def __init__(self, name, network):
        super().__init__(name)
        self.network = network

    def play_one_action(self, views):

        results = self.network.feedforward(views)
        cumulative_proba = cumsum(results)

        rand = uniform(0, 1)
        action = searchsorted(cumulative_proba, rand)
        return action

    def play_one_action_random(self, views):
        self.network.feedforward(views)
        return randint(0, 3)

