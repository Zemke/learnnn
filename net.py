#!/usr/bin/env python3

import os

from math import sqrt

import torch
import torch.nn as nn
import torch.nn.functional as F

import data
from minmax import MinMaxNorm

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
  return res


def norm_bounded(x, mn_p, mx_p, a, b):
  return a + (((x - mn_p) * (b - a)) / (mx_p - mn_p))


if __name__ == "__main__":
  net = Net()

  if os.environ.get('TRAIN', '1') == '1':
    print(net)
    epochs = int(os.environ.get('EPOCHS', 500));
    print(f'training on {epochs} epochs');
    train(net, epochs)

  s = os.environ.get('INFER', '-1')
  if s != '-1':
    res = infer(net, data.NNNData(s))
    [print(x) for x in sorted(res)]

  if os.environ.get('ASSESS', '0') == '1':
    for s in ['39', '40', '41current']:
      ds = data.NNNData(s)
      mmn = MinMaxNorm()([ds])
      mx_r, mn_r = mmn.y_maxs, mmn.y_mins
      res = infer(net, ds)
      mn_p, mx_p = min([p for p,_ in res]), max([p for p,_ in res])
      nn = [(norm_bounded(p, mn_p, mx_p, mn_r, mx_r), u) \
        for p,u in res]
      assert min([p for p,_ in nn]) == mn_r
      assert max([p for p,_ in nn]) == mx_r
      diffsum = 0
      for p,u in nn:
        pu_p = [pu['points'] for pu in ds.puu if pu['u'] == u][0]
        diffsum += (p - pu_p) ** 2
      rmse = sqrt(diffsum / len(nn))
      print('rmse', s, rmse)

