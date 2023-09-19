import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

from constants import M, N, K

class Player:
    def __init__(self, id=0):
        self.id = id


    def choose_action(self, game):
        actions = game.get_actions()
        return random.choice(actions)


class AIPlayer(Player):

    def __init__(self, id=0):
        Player.__init__(self, id=id)
        self.experience = []

        class Net(nn.Module):
            def __init__(self):
                super(Net, self).__init__()
                # 1 input image channel, 6 output channels, 5x5 square convolution
                # kernel
                self.conv1 = nn.Conv2d(1, 2*K + 2, K)
                # self.conv2 = nn.Flatten(10, 16, 5)
                # an affine operation: y = Wx + b
                self.fc1 = nn.Linear((M - K + 1) * (N - K + 1) * (2*K + 2), N * N)  # 5*5 from image dimension
                self.fc2 = nn.Linear(N * N, N)

            def forward(self, x):
                # Max pooling over a (2, 2) window
                x = F.relu(self.conv1(x))
                # If the size is a square, you can specify with a single number
                # x = F.max_pool2d(F.relu(self.conv2(x)), 2)
                x = torch.flatten(x, 1)  # flatten all dimensions except the batch dimension
                x = F.relu(self.fc1(x))
                x = self.fc2(x)
                return x

        self.net = Net()

    def choose_action(self, game):
        out = self.net(torch.unsqueeze(torch.unsqueeze(
            torch.from_numpy(game.grid).float(), 0), 0))
        action_ratings = out.detach().numpy().flatten()
        available_actions = game.get_actions()
        best_action = max(available_actions, key=lambda i: action_ratings[i])
        return best_action