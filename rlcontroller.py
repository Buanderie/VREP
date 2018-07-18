
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Actor(nn.Module):
    def __init__(self, num_actions):
        super(Actor, self).__init__()
        self.num_actions = num_actions
        self.dense_1 = nn.Linear(4, 32)
        self.out = nn.Linear(32, num_actions)

    def forward(self, x):
        x = self.dense_1(x)
        x = F.softmax(self.out(x))
        return x


class Critic(nn.Module):
    def __init__(self):
        super().__init__()
        self.dense_1 = nn.Linear(4, 32)
        self.out = nn.Linear(32, 1)

    def forward(self, x):
        x = F.relu(self.dense_1(x))
        x = self.out(x)
        return x
