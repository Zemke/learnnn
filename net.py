#!/usr/bin/env python3

import os

import torch
import torch.nn as nn
import torch.nn.functional as F
from data import NnnData

class Net(nn.Module):

  def __init__(self):
    super(Net, self).__init__()
    self.fc = nn.Sequential(
      nn.Linear(10, 50),
      nn.ReLU(inplace=True),
      nn.Linear(50, 100),
      nn.ReLU(inplace=True),
      nn.Linear(100, 50),
      nn.ReLU(inplace=True),
      nn.Linear(50, 1),
      nn.ReLU(inplace=True),
    )

  def forward(self, x):
    return self.fc(x)


def train(net, epochs):
  # ReLU
  # MSELoss
  # Adam or SGD

  d39 = NnnData(39)
  d39[0]
  return

  optimizer = optim.SGD(net.parameters(), lr=0.01)
  mse = nn.MSELoss()

  for i in range(epochs):
    optimizer.zero_grad()
    #x = 
    y = net(x)
    loss = mse(y, x)
    loss.backward()
    optimizier.step()


if __name__ == "__main__":
  net = Net()
  print(net)
  epochs = os.environ.get('EPOCHS', 500);
  print(f'training on {epochs} epochs');
  train(net, epochs)

