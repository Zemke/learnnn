Can AI learn a foreign ranking system and replicate it?

All of the ranking information 
---

This is all of the information a ranking system has:

* games
  * home user
  * away user
  * won rounds
  * lost rounds

This can be squashed in a per-user view:

* opp
  * won rounds
  * lost rounds

This is considering the NN is run per user.
Also, there's no relevance about who the opponent is.
The only thing important about him is how he is ranked.
Therefore:

* opp ranking
* won rounds
* lost round

That's an accumulated game.
Which is the added won/lost rounds against the same playelayer
That would be one input. Thing is, that it's actually three data points.
Therefore the first layer is should not be fully connected.
So, that input from one accumulated game doesn't cross another.

Stretched out
---

Fully-connected approach.
Inputs are:

* num of won rounds
* num of lost rounds
* rankings of opponents


A whole 'nother take
---

We don't know the params of the formula.
We're just inputting the NN all kinds of variables we can think of.
That's per user.
The input would be data that can be derived from no existing ranking.
I.e. points of opponent users must not be used.
Here are inputs I can think of:

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

The idea is to input as many data as possible even if somewhat redundant.
The NN should figure out itself what's relevant.

NNN Points Analyzer
---

Apparently it works only for pairings where both players are already part of the ranking
(having already played at least one round).

Active players (70 in total) in overall rating are:

```
chuvash, Rafka, PavelB, Dario, Master, Psykologi, Albus, Senator, KinslayeR, Dieego98, Silaneo, Kayz, tita, Perdunok, Free, Rudolf289, tadeusz, Lupastic, Kilobyte, Leoric, Chicken23, Siwy, Thouson, Kano, djongador, MegaAdnan, EPI, pava, Eray, StJimmy, FrancisNgannoy, oldsock, Jago, SIBASA, Abegod, Koras, Cinek, DarK'X'LorD, Gufron, Corujao, Kamazi, Kisiro, Yagelon, dibz, Ledan, Cinzel, Crespo, Ypslon, ILYXA, DurczyN, CzarnyKot, Amanwaf, Roccat, Danelius, russianvodka, TOMT, Still, Ferenando, Jexusjex, VdM2103, DrNick, Knight Templar, Irtis, lopez185, Albino, LacLac, Puschkin, J040, Szwagier, Zhirnich

```

```console
curl 'http://www.normalnonoobs.com/analyzer/docalc' -X POST -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -d 'scores=%7B%22240%22%3A%7B%22838%22%3A%5B0%2C14%5D%7D%2C%22838%22%3A%7B%22240%22%3A%5B14%2C0%5D%7D%7D&season=overall'
```

