#!/usr/bin/env python3

import os
import pandas as pd
from minmax import MinMaxNorm

import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader


DD = os.environ.get('DEBUG', '0') == '1'


class NNNData(Dataset):

  def __init__(self, season, mmn = None):
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
    self.mmn = mmn
    self.labels = pd.read_csv(f'csv/ranking_nnn{season}.tsv', sep='\t')
    self.labels = self.labels[self.labels['Rounds'] != '0-(0)']
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
          'oppOpps': 0,
        }
        opps = []
        DD and print('user ' + u)
        for l in ll:
          if l[0] == u:
            DD and print(f'{l[2]}-{l[3]} {l[1]}')
            pu['won'] += l[2]
            pu['lost'] += l[3]
            pu['opps'].add(l[1])
            pu['total'] += l[2] + l[3]
          elif l[1] == u:
            DD and print(f'{l[3]}-{l[2]} {l[0]}')
            pu['won'] += l[3]
            pu['lost'] += l[2]
            pu['opps'].add(l[0])
            pu['total'] += l[2] + l[3]
        self.puu.append(pu)

      for pu in self.puu:
        DD and print('user opping ' + pu['u'])
        DD and print(len(pu['opps']))
        for uopp in pu['opps']:
          for opp in self.puu:
            if opp['u'] != uopp:
              continue
            DD and print('opp ' + opp['u'])
            pu['oppWon'] += opp['won']
            pu['oppLost'] += opp['lost']
            pu['oppTotal'] += opp['total']
            pu['oppOpps'] += len(opp['opps'])

      self.total = sum([pu['total'] for pu in self.puu]) // 2
      self.total_users = len(self.puu)

      DD and print('total', self.total)
      DD and print('total_users', self.total_users)


  def __len__(self):
    return len(self.labels)


  def __getitem__(self, idx):
    u,p = self.labels.iloc[idx, 1:3]
    pu = [pu for pu in self.puu if pu['u'] == u][0]
    DD and print(pu['u'], p)
    if self.mmn is not None and self.mmn.ready:
      return \
        self.mmn.norm_x(self.to_input(pu)), \
        self.mmn.norm_y(torch.tensor(p).float())
    else:
      return self.to_input(pu), torch.tensor(p).float()


  def to_input(self, pu):
    return torch.tensor([
      pu['won'],
      pu['lost'],
      pu['total'],
      len(pu['opps']),
      pu['oppWon'],
      pu['oppLost'],
      pu['oppTotal'],
      pu['oppOpps'],
      self.total,
      self.total_users,
    ]).float()


def load():
  mmn = MinMaxNorm()
  dss = [NNNData(s, mmn) for s in ['39', '40', '41current']]
  mmn(dss)
  dl = DataLoader(
    dss[0] + dss[1] + dss[2],
    batch_size=int(os.environ.get('BATCH_SIZE', 8)),
    shuffle=True)
  return dl


if __name__ == '__main__':
  pass

