# Description

6 Nimmt is a German game invented in 1994. This program is a simulation of that game. The simulation is run N number of times to determine the best strategy among a combination of strategies.

So far, only simple strategies were simulated, namely RND (the player chooses a random card), LARG (the player always chooses the largest card), SMA (the player always chooses the smallest card).


# Results
Even with these simple strategies, the chance of winning is not always straightforward to deduce. With only 2 players, it looks like a random strategy is the best of the three. With 3 or more players, it seems that LARG often takes the upper hand, provided another player is also playing LARG, thus the strategies reinforce each other. Otherwise, SMA takes the upper hand. Not all possible number of players and combinations have been simulated.

# Future development
It is not my intention to recreate the game for the purpose of playing, an endeavor that would require building a GUI, and potentially hosting the game app on a server. Someone has already beat me to it anyway. Instead, I am merely interested in different strategies and how they fair against each other. I would be also interested to learn about the underlying mathematics that could explain the results.

Next, I will be working on simulating more elaborate strategies that are closer to how real players would approach the game.
