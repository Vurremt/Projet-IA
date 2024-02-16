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

        if winner == 1:
            if type(self.player1) == AIPlayer :
                self.player1.network.states_rewards[-1] = 1
                # Good score + backpropagation player1
                pass
            if type(self.player2) == AIPlayer :
                self.player2.network.states_rewards[-1] = -1
                # Bad score + backpropagation player2
                pass
            if display : print(f"Player 1 {player1.name} won!")
        if winner == 2:
            if type(self.player2) == AIPlayer :
                self.player2.network.states_rewards[-1] = 1
                # Good score + backpropagation player2
                pass
            if type(self.player1) == AIPlayer :
                self.player1.network.states_rewards[-1] = -1
                # Bad score + backpropagation player1
                pass
            if display : print(f"Player 2 {player2.name} won!")
        if winner == 3:
            if type(self.player1) == AIPlayer :
                self.player1.network.states_rewards[-1] = -0.5
                # Medium score + backpropagation player1
                pass
            if type(self.player2) == AIPlayer :
                self.player2.network.states_rewards[-1] = -0.5
                # Medium score + backpropagation player2
                pass
            if display : print("Draw !")



player1 = HumanPlayer("Evahn")

model = Network_RL()
model.addLayer( Linear(42, 50) )
model.addLayer( Sigmoid() )
model.addLayer( Linear(50, 7 ))
model.addLayer( Sigmoid() )
player2 = AIPlayer("Yui", model)

c = Connect4(player1,player2)

c.game_loop(display=True)

print(player2.network.states_rewards[-1], player2.network.states_inputs[-1])
