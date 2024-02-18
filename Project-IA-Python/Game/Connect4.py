import numpy as np
from Player import *
from Reseau import *

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

    def play_one_turn(self, display):
        self.round += 1
        if (self.round + 1) % 2 == 0:
            current_player = self.player1
        else:
            current_player = self.player2

        if display :
            print(f"---- Round {self.round} : {current_player.name} turn ----")
            if type(current_player) == HumanPlayer : print("Choise : ",end ='')

        input_player = self.recup_action(current_player) - 1
        while self.full_col(input_player) :
            if display and type(current_player) == HumanPlayer: print("Choise : ", end ='')
            input_player = self.recup_action(current_player) - 1

        line_i = self.add_token(input_player)

        if display : self.displayGrid()

        if self.is_winner(input_player, line_i, ((self.round + 1) % 2) + 1) : return ((self.round + 1) % 2) + 1
        elif self.full_grid() : return 3
        else : return 0

    def game_loop(self, display):
        if display : self.displayGrid()

        winner = 0
        while winner == 0:
            winner = self.play_one_turn(display)

        if display and winner == 1: print(f"Player 1 {self.player1.name} won!")
        if display and winner == 2: print(f"Player 2 {self.player2.name} won!")
        if display and winner == 3: print("Draw !")
        return winner


def play_game_vs_random(player_ai, player_random, nb_games):
    lose = 0
    win = 0
    draw = 0
    for i in range(nb_games):
        if(randint(0,1) == 1):
            player1 = player_ai
            player2 = player_random
            c = Connect4(player1, player2)
            winner = c.game_loop(display=False)
            if winner == 1 :
                win += 1
            if winner == 2 :
                lose += 1
            if winner == 3 :
                draw += 1
        else:
            player1 = player_random
            player2 = player_ai
            c = Connect4(player1, player2)
            winner = c.game_loop(display=False)
            if winner == 1:
                lose += 1
            if winner == 2:
                win += 1
            if winner == 3:
                draw += 1
    print(f"Win rate = {int((win / (win + lose + draw)) * 100)}%")


def fit_game(player_1, player_2, nb_games, factor, start_learning_rate, end_learning_rate, step_learning_rate):

    learning_rate = start_learning_rate
    for i in range(nb_games):
        print(f"Game {i}", end='')
        player_1.network.clear_states()
        player_2.network.clear_states()
        if (randint(0, 1) == 1):
            player1 = player_1 # !!!!!!!!!!!! Attention il faut par reference, pas par copie !!!!!!!!!!!
            player2 = player_2
        else:
            player1 = player_2
            player2 = player_1

        c = Connect4(player1, player2)
        winner = c.game_loop(display=False)
        del c
        print(f", winner : {winner}")

        if winner == 1:
            player1.network.update_all_states(1, factor, learning_rate)
            player2.network.update_all_states(-1, factor, learning_rate)

        if winner == 2:
            player2.network.update_all_states(1, factor, learning_rate)
            player1.network.update_all_states(-1, factor, learning_rate)

        if winner == 3:
            player1.network.update_all_states(-0.5, factor, learning_rate)
            player2.network.update_all_states(-0.5, factor, learning_rate)

        if i % 100 == 0:
            player_1.network.save("../player1.txt")
            player_2.network.save("../player2.txt")
            playerRand = RandomPlayer("Rand")
            print("Player 1 ", end = '')
            play_game_vs_random(player_1, playerRand, 100)
            print("Player 2 ", end='')
            play_game_vs_random(player_2, playerRand, 100)
            print()

        if learning_rate > end_learning_rate:
            learning_rate -= step_learning_rate



#player1 = HumanPlayer("Evahn")


model = Network_RL()
model.addLayer( Linear(42, 50) )
model.addLayer( Sigmoid() )
model.addLayer( Linear(50, 7 ))
model.addLayer( Sigmoid() )
model.addLayer( Proba_output() )
player_1 = AIPlayer("P1", model)

model2 = Network_RL()
model2.addLayer( Linear(42, 50) )
model2.addLayer( Sigmoid() )
model2.addLayer( Linear(50, 7 ))
model2.addLayer( Sigmoid() )
model2.addLayer( Proba_output() )
player_2 = AIPlayer("P2", model2)



fit_game(player_1, player_2, 100000, 0.5, 0.95, 0.05, 0.00001)
