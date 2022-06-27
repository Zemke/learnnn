#!/usr/bin/env python3

import os

import torch
import torch.nn as nn
import torch.nn.functional as F
import data

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
      #nn.ReLU(inplace=True),
    )

  def forward(self, x):
    return self.fc(x)


def train(net, epochs):
  optim = torch.optim.SGD(net.parameters(), lr=0.01)
  mse = nn.MSELoss()
  dl = data.load()

  for epoch in range(epochs):
    for i,(x,y) in enumerate(dl):
      optim.zero_grad()
      res = net(x)
      loss = mse(res, y)
      loss.backward()
      optim.step()


if __name__ == "__main__":
  net = Net()
  print(net)
  epochs = os.environ.get('EPOCHS', 500);
  print(f'training on {epochs} epochs');
  train(net, epochs)

