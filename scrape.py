#!/usr/bin/env python3

"""
lair@csv cat games_nnn39.csv | grep -o ',[0-9],[0-9]' | cut -b2- | sed 's/,/+/' | xargs -n1 -I% echo +% | xargs | cut -b2- | bc
1348
lair@csv cat games_nnn40.csv | grep -o ',[0-9],[0-9]' | cut -b2- | sed 's/,/+/' | xargs -n1 -I% echo +% | xargs | cut -b2- | bc
1096
lair@csv cat games_nnn41current.csv | grep -o ',[0-9],[0-9]' | cut -b2- | sed 's/,/+/' | xargs -n1 -I% echo +% | xargs | cut -b2- | bc
184
"""

# max total rounds could be 3600 because that would equal about 10 games of four rounds per day

# up to 1400 rounds
# no inputs where one user won all rounds of all total rounds played

# users available for modifying results for
# only users with games played can be analyzed points for
# these are from the overall ranking
USERS = [
  'chuvash', 'Rafka', 'PavelB', 'Dario', 'Master', 'Psykologi', 'Albus', 'Senator', 'KinslayeR', 'Dieego98', 'Silaneo', 'Kayz', 'tita', 'Perdunok', 'Free', 'Rudolf289', 'tadeusz', 'Lupastic', 'Kilobyte', 'Leoric', 'Chicken23', 'Siwy', 'Thouson', 'Kano', 'djongador', 'MegaAdnan', 'EPI', 'pava', 'Eray', 'StJimmy', 'FrancisNgannoy', 'oldsock', 'Jago', 'SIBASA', 'Abegod', 'Koras', 'Cinek', "DarK'X'LorD", 'Gufron', 'Corujao', 'Kamazi', 'Kisiro', 'Yagelon', 'dibz', 'Ledan', 'Cinzel', 'Crespo', 'Ypslon', 'ILYXA', 'DurczyN', 'CzarnyKot', 'Amanwaf', 'Roccat', 'Danelius', 'russianvodka', 'TOMT', 'Still', 'Ferenando', 'Jexusjex', 'VdM2103', 'DrNick', 'Knight Templar', 'Irtis', 'lopez185', 'Albino', 'LacLac', 'Puschkin', 'J040', 'Szwagier', 'Zhirnich']

assert len(USERS) == 70

# TODO scrape data from NNN points analyzer

for i in range(10_000):
  pass

