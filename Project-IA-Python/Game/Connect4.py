import numpy as np

from Player import *
from Reseau import *
import random
import time

class Connect4:
    def __init__(self, player1, player2):
        self.grid = np.zeros((6,7), dtype=int)
        self.current_col = np.full(7, 5, dtype=int)
        self.player1 = player1
        self.player2 = player2
        self.round = 0

    def add_token(self, col_i):
        self.grid[self.current_col[col_i]][col_i] = ((self.round + 1) % 2) + 1
        self.current_col[col_i] -= 1
        return self.current_col[col_i] + 1

    def full_col(self, col_i):
        if col_i < 0 or col_i > 6 : return True
        return self.current_col[col_i] < 0

    def recup_action(self, player):
        return player.play_one_action(self.grid)

    def displayGrid(self):
        print("--1-2-3-4-5-6-7--")
        for i in range(self.grid.shape[0]):
            print("|", end ='')
            for j in range(self.grid.shape[1]):
                print(f" {self.grid[i][j]}", end ='')
            print(" |")
        print("-----------------")

    def full_grid(self):
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i][j] == 0 : return False
        return True

    def is_winner(self, col, line, num_player):
        # Horizontal check
        for i in range(4):
            if col - i >= 0 and col - i + 3 < 7:
                if (self.grid[line][col - i] == num_player and self.grid[line][col - i + 1] == num_player and
                        self.grid[line][col - i + 2] == num_player and self.grid[line][col - i + 3] == num_player):
                    return True

        # Vertical check
        if line <= 2:
            if (self.grid[line][col] == num_player and self.grid[line + 1][col] == num_player and
                    self.grid[line + 2][col] == num_player and self.grid[line + 3][col] == num_player):
                return True

        # Diagonal check (bottom left to top right)
        for i in range(4):
            if col - i >= 0 and col - i + 3 < 7 and line - i >= 0 and line - i + 3 < 6:
                if (self.grid[line - i][col - i] == num_player and self.grid[line - i + 1][
                    col - i + 1] == num_player and
                        self.grid[line - i + 2][col - i + 2] == num_player and self.grid[line - i + 3][
                            col - i + 3] == num_player):
                    return True

        # Diagonal check (top left to bottom right)
        for i in range(4):
            if col - i >= 0 and col - i + 3 < 7 and line + i - 3 >= 0 and line + i < 6:
                if (self.grid[line + i][col - i] == num_player and self.grid[line + i - 1][
                    col - i + 1] == num_player and
                        self.grid[line + i - 2][col - i + 2] == num_player and self.grid[line + i - 3][
                            col - i + 3] == num_player):
                    return True

        # If no win condition is met, return False
        return False

    def play_one_turn(self):
        self.round += 1
        if (self.round + 1) % 2 == 0:
            current_player = self.player1
        else:
            current_player = self.player2

        print(f"---- Round {self.round} : {current_player.name} turn ----")
        print("Choise : ",end ='')

        input_player = self.recup_action(current_player) - 1
        if(type(current_player) == AIPlayer or type(current_player) == RandomPlayer): print(input_player + 1)
        while self.full_col(input_player) :
            if type(current_player) == AIPlayer or type(current_player) == RandomPlayer :
                free_col = list()
                for i in range(len(self.current_col)):
                    if self.current_col[i] >= 0: free_col.append(i)
                input_player = random.choice(free_col)
                print(f"Choise : {input_player + 1}")
                break
            print("Choise : ", end ='')
            input_player = self.recup_action(current_player) - 1

        line_i = self.add_token(input_player)

        self.displayGrid()

        if self.is_winner(input_player, line_i, ((self.round + 1) % 2) + 1) : return ((self.round + 1) % 2) + 1
        elif self.full_grid() : return 3
        else : return 0

    def game_loop(self):
        self.displayGrid()

        winner = 0
        while winner == 0:
            winner = self.play_one_turn()

        if winner == 1: print(f"Player 1 {self.player1.name} won!")
        if winner == 2: print(f"Player 2 {self.player2.name} won!")
        if winner == 3: print("Draw !")
        return winner

    def reset_game(self, player1, player2):
        self.grid = np.zeros((6, 7), dtype=int)
        self.current_col = np.full(7, 5, dtype=int)
        self.player1 = player1
        self.player2 = player2
        self.round = 0


class Connect4Training(Connect4):
    def play_one_turn_training(self):
        self.round += 1
        if (self.round + 1) % 2 == 0:
            current_player = self.player1
        else:
            current_player = self.player2

        input_player = self.recup_action(current_player) - 1
        if self.full_col(input_player) :
            free_col = list()
            for i in range(len(self.current_col)):
                if self.current_col[i] >= 0 : free_col.append(i)
            input_player = random.choice(free_col)

        line_i = self.add_token(input_player)

        if self.is_winner(input_player, line_i, ((self.round + 1) % 2) + 1) : return ((self.round + 1) % 2) + 1
        elif self.full_grid() : return 3
        else : return 0

    def game_loop_training(self):
        winner = 0

        while winner == 0:
            winner = self.play_one_turn_training()

        return winner, self.round



def play_game_vs_random(player_ai, nb_games):
    lose = 0
    win = 0
    draw = 0
    game = Connect4Training(None, None)
    player_random = RandomPlayer("Rand")
    for i in range(nb_games):
        if randint(0, 1) == 1:
            game.reset_game(player_ai, player_random)
            winner, round = game.game_loop_training()
            if winner == 1 :
                win += 1
            if winner == 2 :
                lose += 1
            if winner == 3 :
                draw += 1
        else:
            game.reset_game(player_random, player_ai)
            winner, round = game.game_loop_training()
            if winner == 1:
                lose += 1
            if winner == 2:
                win += 1
            if winner == 3:
                draw += 1
    print(f"Win rate = {int((win / (win + lose + draw)) * 100)}%")
    del player_random
    del game


def fit_game(player_1, player_2, nb_games, factor, start_learning_rate, end_learning_rate, step_learning_rate):

    learning_rate = start_learning_rate
    game = Connect4Training(None, None)

    for i in range(nb_games+1):
        player_1.network.clear_states()
        player_2.network.clear_states()
        if randint(0, 1) == 1:

            game.reset_game(player_1, player_2)
            winner, round = game.game_loop_training()

            reward = (round - 7) * -0.014
            if winner == 1:
                player_1.network.update_all_states(1 + reward, factor, learning_rate)
                player_2.network.update_all_states(-1 + reward, factor, learning_rate)

            if winner == 2:
                player_2.network.update_all_states(1 + reward, factor, learning_rate)
                player_1.network.update_all_states(-1 + reward, factor, learning_rate)

            if winner == 3:
                player_1.network.update_all_states(-0 + reward, factor, learning_rate)
                player_2.network.update_all_states(-0 + reward, factor, learning_rate)

        else:

            game.reset_game(player_2, player_1)
            winner, round = game.game_loop_training()

            reward = (round - 7) * -0.014
            if winner == 1:
                player_2.network.update_all_states(1 + reward, factor, learning_rate)
                player_1.network.update_all_states(-1 + reward, factor, learning_rate)

            if winner == 2:
                player_1.network.update_all_states(1 + reward, factor, learning_rate)
                player_2.network.update_all_states(-1 + reward, factor, learning_rate)

            if winner == 3:
                player_1.network.update_all_states(-0 + reward, factor, learning_rate)
                player_2.network.update_all_states(-0 + reward, factor, learning_rate)

        if i % 10000 == 0:
            print(f"--------------------\n{i} games played")
            player_1.network.save("../save_brain/player1_{0}iter_{1:.2f}lr.txt".format(i, learning_rate))
            player_2.network.save("../save_brain/player2_{0}iter_{1:.2f}lr.txt".format(i, learning_rate))
            print("Player 1 ", end = '')
            play_game_vs_random(player_1, 100)
            print("Player 2 ", end='')
            play_game_vs_random(player_2, 100)
            print()

        if learning_rate > end_learning_rate:
            learning_rate -= step_learning_rate

    del game


model = Network_RL()
model.addLayer( Linear(42, 50) )
model.addLayer( ReLU() )
model.addLayer( Linear(50, 50 ))
model.addLayer( Linear(50, 50 ))
model.addLayer( Linear(50, 50 ))
model.addLayer( Linear(50, 7 ))
model.addLayer( ReLU() )
model.addLayer( Softmax() )
player_1 = AIPlayer("P1", model)

model2 = Network_RL()
model2.addLayer( Linear(42, 50) )
model2.addLayer( Sigmoid() )
model2.addLayer( Linear(50, 50 ))
model2.addLayer( Sigmoid() )
model2.addLayer( Linear(50, 50 ))
model2.addLayer( Sigmoid() )
model2.addLayer( Linear(50, 50 ))
model2.addLayer( Sigmoid() )
model2.addLayer( Linear(50, 7 ))
model2.addLayer( Sigmoid() )
model2.addLayer( Softmax() )
player_2 = AIPlayer("P2", model2)

fit_game(player_1, player_2, 100000, 1, 0.95, 0.05, 0.00001)

"""
player1 = HumanPlayer("Evahn")
model = Network_RL()
player_2 = AIPlayer("P2", model)
player_2.network.load("../save_brain/player1_100000iter_0.05lr.txt")

game = Connect4(player1, player_2)
game.game_loop()
"""
