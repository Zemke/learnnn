#!/usr/bin/env python3

import os

from math import sqrt

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
    )

  def forward(self, x):
    return self.fc(x)


def train(net, epochs):
  optim = torch.optim.SGD(
    net.parameters(),
    lr=1e-2,
    weight_decay=1e-5,
    momentum=0.9)
  mse = nn.MSELoss()
  dl = data.load()

  losses_metric = []
  for epoch in range(epochs):
    for i,(x,y) in enumerate(dl):
      optim.zero_grad()
      net.train(True)
      y_pred = net(x)
      loss = mse(y_pred.squeeze(), y)
      loss.backward()
      sqrt_loss = sqrt(loss.item())
      print(sqrt_loss)
      losses_metric.append(sqrt_loss)
      optim.step()

  print(losses_metric)
  if os.environ.get('PLT', '0') == '1':
    import matplotlib.pyplot as plt
    #plt.ylim(top=1000)
    plt.plot(losses_metric)
    plt.show()


@torch.no_grad()
def infer(net, ds):
  res = []
  for pu in ds.puu:
    net.eval()
    y_pred = net(ds.to_input(pu)).item()
    res.append((y_pred, pu['u']))
  print(sorted(res))


if __name__ == "__main__":
  net = Net()
  print(net)
  epochs = int(os.environ.get('EPOCHS', 500));
  print(f'training on {epochs} epochs');
  train(net, epochs)
  if os.environ.get('INFER', '0') == '1':
    infer(net, data.NNNData('39'))

