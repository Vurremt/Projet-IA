from abc import ABC, abstractmethod
from numpy import ravel, sum, cumsum, searchsorted
from random import uniform

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
    def __init__(self, name, network):
        super().__init__(name)
        self.network = network

    def play_one_action(self, grid):
        input = ravel(grid)
        self.network.add_state(0, input)
        print(self.network.states_rewards[-1], self.network.states_inputs[-1])

        results = self.network.feedforward(input)
        proba_results = results / sum(results)
        cumulative_proba = cumsum(proba_results)

        rand = uniform(0, 1)
        action = searchsorted(cumulative_proba, rand)
        return action + 1  # +1 for being between 1 and 7

