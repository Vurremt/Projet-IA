import numpy as np

from Player import *
from Reseau import *
import random
import time

class Labyrinth:
    def __init__(self, player):
        self.grid = np.array([[0,1,2,0,0],
                                [2,0,0,1,2]])
        self.player = player
        self.pos_player = [0,0]
        self.nb_objectives = 3
        self.score = 0
        self.round = 0

    def displayGrid(self):
        print("-" + (self.grid.shape[1] + 1) * "--")
        for i in range(self.grid.shape[0]):
            print("|", end='')
            for j in range(self.grid.shape[1]):
                if i == self.pos_player[0] and j == self.pos_player[1]:
                    print(" X", end='')
                else:
                    print(f" {self.grid[i][j]}", end='')
            print(" |")
        print("-" + (self.grid.shape[1] + 1) * "--")
        print()

    def play_one_turn(self, learning_rate, epsilon, display):

        if display : print(f"Tour {self.round} : ", end ='')

        views = list()

        #Nord
        if self.pos_player[0] < 1 : views.append(1)
        else : views.append(self.grid[self.pos_player[0] - 1][self.pos_player[1]])

        #Est
        if self.pos_player[1] > self.grid.shape[1] - 2 : views.append(1)
        else : views.append(self.grid[self.pos_player[0]][self.pos_player[1] + 1])

        #Ouest
        if self.pos_player[0] > self.grid.shape[0] - 2 : views.append(1)
        else : views.append(self.grid[self.pos_player[0] + 1][self.pos_player[1]])

        #Sud
        if self.pos_player[1] < 1 : views.append(1)
        else : views.append(self.grid[self.pos_player[0]][self.pos_player[1] - 1])

        if uniform(0,1) < epsilon:
            action = self.player.play_one_action_random(views)
        else:
            action = self.player.play_one_action(views)

        if action == 0 :
            if display : print("Nord")
            if self.pos_player[0] >= 1 :self.pos_player[0] -= 1
            else :
                self.score -= 1
                self.player.network.backpropagation(-1)
                self.player.network.update(learning_rate)

        elif action == 1 :
            if display : print("Est")
            if self.pos_player[1] <= self.grid.shape[1] - 2 : self.pos_player[1] += 1
            else :
                self.score -= 1
                self.player.network.backpropagation(-1)
                self.player.network.update(learning_rate)

        elif action == 2 :
            if display : print("Sud")
            if self.pos_player[0] <= self.grid.shape[0] - 2 : self.pos_player[0] += 1
            else :
                self.score -= 1
                self.player.network.backpropagation(-1)
                self.player.network.update(learning_rate)

        elif action == 3 :
            if display : print("Ouest")
            if self.pos_player[1] >= 1 : self.pos_player[1] -= 1
            else :
                self.score -= 1
                self.player.network.backpropagation(-1)
                self.player.network.update(learning_rate)


        if self.grid[self.pos_player[0]][self.pos_player[1]] == 2:
            self.grid[self.pos_player[0]][self.pos_player[1]] = 0
            self.nb_objectives -= 1
            self.player.network.backpropagation(10)
            self.score += 10
            self.player.network.update(learning_rate)
        elif self.grid[self.pos_player[0]][self.pos_player[1]] == 1:
            self.grid[self.pos_player[0]][self.pos_player[1]] = 0
            self.player.network.backpropagation(-10)
            self.score -= 10
            self.player.network.update(learning_rate)

        if display : self.displayGrid()

        if self.nb_objectives == 0:
            return 1
        if self.round == 100:
            return 2
        return 0


    def game_loop(self, learning_rate, epsilon, display):
        if display : self.displayGrid()

        end = 0
        while not end:
            self.round += 1
            end = self.play_one_turn(learning_rate, epsilon, display)

        return end

    def reset_game(self):
        self.grid = np.array([[0,1,2,0,0],
                                [2,0,0,1,2]])
        self.nb_objectives = 3
        self.pos_player = [0,0]
        self.score = 0
        self.round = 0


def fit_game(player, nb_games, learning_rate, start_epsilon, end_epsilon, step_epsilon):

    game = Labyrinth(player)
    epsilon = start_epsilon

    average_round = 0
    average_score = 0
    for i in range(1, nb_games+1):

        end = game.game_loop(learning_rate, epsilon, False)
        if end == 1:
            print(f"Partie {i} reussie en {game.round} coups avec epsilon de " + "{:.2f}".format(epsilon) + f" avec un score de {game.score}")
            average_round += game.round
        else:
            average_round += 100
        average_score += game.score


        if i % 100 == 0:
            print(f"{i} games played")
            print(f"Average round on 100 last games : {average_round / 100}")
            print(f"Average score on 100 last games : {average_score / 100}\n")
            average_score = 0
            average_round = 0

        if epsilon > end_epsilon:
            epsilon -= step_epsilon

        game.reset_game()

    del game


model = Network_RL()
model.addLayer( Linear(4, 30) )
model.addLayer( ReLU() )
model.addLayer( Linear(30, 30) )
model.addLayer( ReLU() )
model.addLayer( Linear(30, 4 ))
model.addLayer( ReLU() )
model.addLayer( Softmax() )
player = AIPlayerLabyrinth("PlayerAI", model)

fit_game(player, 100000, 0.05, 1, 0.01, 0.00001)

