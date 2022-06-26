#!/usr/bin/env python3

import os
import pandas as pd
from torch.utils.data import Dataset
from torchvision import datasets


class PerUser:

  def __init__(self, u):
    self.u = u
    self.won = 0
    self.lost = 0
    self.total = 0
    self.opps = set()


  def __repr__(self):
    return f'PerUser(u={u}, won={won}, lost={lost}, '


class NnnData(Dataset):

  def __init__(self, season):
    """
    * user
      * won rounds
      * lost rounds
      * total rounds
      * num of opponents
    * opponents
      * won rounds
      * lost rounds
      * total rounds
      * num of opponents
    * totals
      * total rounds
      * total users (with games played)
    """
    self.labels = pd \
      .read_csv(f'csv/ranking_nnn{season}.tsv', sep='\t') \
      .sample(frac=1).reset_index(drop=True)  # shuffle
    with open(f'csv/games_nnn{season}.csv', 'r') as f:
      ll = [(l[3], l[4], int(l[1]), int(l[2])) for l in
        [l.split(',') for l in f.read().splitlines()[1:]]]

    self.puu = []
    for l in ll:
      for u in l[:2]:
        if u in [pu['u'] for pu in self.puu]:
          continue
        pu = {
          'u': u,
          'won': 0,
          'lost': 0,
          'total': 0,
          'opps': set(),
          'oppWon': 0,
          'oppLost': 0,
          'oppTotal': 0,
        }
        opps = []
        print('user ' + u)
        for l in ll:
          if l[0] == u:
            print(f'{l[2]}-{l[3]} {l[1]}')
            pu['won'] += l[2]
            pu['lost'] += l[3]
            pu['opps'].add(l[1])
            pu['total'] += l[2] + l[3]
          elif l[1] == u:
            print(f'{l[3]}-{l[2]} {l[0]}')
            pu['won'] += l[3]
            pu['lost'] += l[2]
            pu['opps'].add(l[0])
            pu['total'] += l[2] + l[3]
        self.puu.append(pu)

      for pu in self.puu:
        print('user opping ' + pu['u'])
        print(len(pu['opps']))
        for uopp in pu['opps']:
          for opp in self.puu:
            if opp['u'] != uopp:
              continue
            print('opp ' + opp['u'])
            pu['oppWon'] += opp['won']
            pu['oppLost'] += opp['lost']
            pu['oppTotal'] += opp['total']

      self.total = sum([pu['total'] for pu in self.puu]) // 2
      self.total_users = len(self.puu)

      print('total', self.total)
      print('total_users', self.total_users)


  def __len__(self):
    return len(self.csv)


  def __getitem__(self, idx):
    dat = self.labels.iloc[idx, 1:3]
    u,p = dat[0], round(float(dat[1]))
    pu = [pu for pu in self.puu if pu['u'] == u][0]
    print(pu['u'], p)
    return [
      pu['won']
      pu['lost']
      pu['total']
      len(pu['opps'])
      pu['oppWon']
      pu['oppLost']
      pu['oppTotal']
    ], p

