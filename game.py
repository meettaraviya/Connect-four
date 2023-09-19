import numpy as np
from termcolor import colored

from player import Player
from constants import M, N, K

class Game:
    def __init__(self, players=None):
        self.grid = np.zeros((M, N), dtype=int)
        self.turn = 0

        if players is None:
            self.players = [Player(id=0), Player(id=1)]
        else:
            self.players = players

    def show(self):
        for i in range(M):
            # print(colored('[', 'white', 'on_blue', attrs=['bold', 'dark']), end='')
            text = ''
            for j in range(N):
                text += colored('(', 'white', 'on_blue', attrs=[])
                if self.grid[i][j] == 1:
                    text += colored('@', 'red', 'on_blue', attrs=['bold'])
                elif self.grid[i][j] == -1:
                    text += colored('@', 'yellow', 'on_blue', attrs=['bold'])
                else:
                    text += colored(' ', 'white', 'on_blue', attrs=['bold'])
                text += colored(')', 'white', 'on_blue', attrs=[])
                # print(text, end='')
            # print(colored(']', 'white', 'on_blue', attrs=['bold', 'dark']), end='\n')
            print(text)

    def get_actions(self):
        return [i for i in range(N) if self.grid[0][i] == 0]

    def take_action(self, action):
        i = M - 1
        while self.grid[i][action] != 0:
            i -= 1
        self.grid[i][action] = 1 if self.turn == 0 else -1
        self.turn = (self.turn + 1) % 2

    def winner(self):
        for player, my_digit in [(0, 1), (1, -1)]:
            for i in range(M):
                chain_length = 0
                for j in range(N):
                    if self.grid[i][j] == my_digit:
                        chain_length += 1
                        if chain_length == K:
                            return player
                    else:
                        chain_length = 0
            for j in range(N):
                chain_length = 0
                for i in range(M):
                    if self.grid[i][j] == my_digit:
                        chain_length += 1
                        if chain_length == K:
                            return player
                    else:
                        chain_length = 0
            for ij_sum in range(K - 1, M + N - K):
                chain_length = 0
                for i in range(max(0, ij_sum - N + 1), min(M - 1, ij_sum) + 1):
                    j = ij_sum - i
                    if self.grid[i][j] == my_digit:
                        chain_length += 1
                        if chain_length == K:
                            return player
                    else:
                        chain_length = 0
            for ij_diff in range(K - N, M - K + 1):
                chain_length = 0
                for i in range(max(0, ij_diff), min(M - 1, N - 1 + ij_diff) + 1):
                    j = i - ij_diff
                    if self.grid[i][j] == my_digit:
                        chain_length += 1
                        if chain_length == K:
                            return player
                    else:
                        chain_length = 0
        return -1


