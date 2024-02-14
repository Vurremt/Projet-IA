import numpy as np
from Player import *

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

    def is_winner(self):
        return False

    def play_one_turn(self, display):
        self.round += 1
        if (self.round + 1) % 2 == 0:
            current_player = self.player1
        else:
            current_player = self.player2

        if display :
            print(f"------ Round {self.round} ------")
            if type(current_player) == HumanPlayer : print("Choise : ",end ='')

        input_player = self.recup_action(current_player) - 1
        while self.full_col(input_player) :
            if display and type(current_player) == HumanPlayer: print("Choise : ", end ='')
            input_player = self.recup_action(current_player) - 1

        line_i = self.add_token(input_player)

        if display : self.displayGrid()

        if self.is_winner() : return ((self.round + 1) % 2) + 1
        elif self.full_grid() : return 3
        else : return 0

    def game_loop(self, display):
        if display : self.displayGrid()

        winner = 0
        while(winner == 0):
            winner = self.play_one_turn(display)

        if(winner == 1):
            if type(self.player1) == AIPlayer :
                # Good score + backpropagation player1
                pass
            if type(self.player2) == AIPlayer :
                # Bad score + backpropagation player2
                pass
            if display : print("Player 1 won!")
        if(winner == 2):
            if type(self.player2) == AIPlayer :
                # Good score + backpropagation player2
                pass
            if type(self.player1) == AIPlayer :
                # Bad score + backpropagation player1
                pass
            if display : print("Player 2 won!")
        if(winner == 3):
            if type(self.player1) == AIPlayer :
                # Medium score + backpropagation player1
                pass
            if type(self.player2) == AIPlayer :
                # Medium score + backpropagation player2
                pass
            if display : print("Draw !")

player1 = HumanPlayer("Evahn")
player2 = HumanPlayer("Paul")
c = Connect4(player1,player2)

c.game_loop(display=True)
