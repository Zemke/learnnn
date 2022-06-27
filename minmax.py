#!/usr/bin/env python3

import torch


class MinMaxNorm:

  def __init__(self):
    self.ready = False

  def __call__(self, dd):
    ss = [torch.stack([x for x,_ in d], 0) for d in dd]
    cat = torch.cat(ss, 0)
    self.x_mins = cat.min(dim=0).values
    self.x_maxs = cat.max(dim=0).values

    ss = [torch.stack([y for _,y in d], 0) for d in dd]
    cat = torch.cat(ss, 0)
    self.y_mins = cat.min(dim=0).values
    self.y_maxs = cat.max(dim=0).values

    self.ready = True
    return self


  def norm_x(self, x):
    return (x - self.x_mins) / (self.x_maxs - self.x_mins)


  def norm_y(self, y):
    return (y - self.y_mins) / (self.y_maxs - self.y_mins)


if __name__ == '__main__':
  mmn = MinMaxNorm()

  print('x_mins', mmn.x_mins)
  print('x_maxs', mmn.x_maxs)
  print('y_mins', mmn.y_mins)
  print('y_maxs', mmn.y_maxs)

  print('norm_x max', mmn.norm_x(mmn.x_maxs))
  print('norm_x min', mmn.norm_x(mmn.x_mins))

  print('norm_y max', mmn.norm_y(mmn.y_maxs))
  print('norm_y min', mmn.norm_y(mmn.y_mins))

