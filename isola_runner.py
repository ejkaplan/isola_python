'''
Created on Nov 9, 2017

@author: eliotkaplan
'''

from isola_game import isola_game
from random_player import random_player
from human_player import human_player
from random import shuffle

def play_game(p1, p2, verbose=False, log=False, time_limit_1=None, time_limit_2=None):
    g = isola_game(p1,p2, time_limit_1, time_limit_2)
    return g.play_game(verbose, log)

def play_tournament(games_per_pairing, *players, verbose=False, log=False, time_limit=None):
    wins = {p:0 for p in players}
    for i in range(len(players)):
        for j in range(i):
            p = [players[i], players[j]]
            shuffle(p)
            for _ in range(games_per_pairing):
                winner = p[play_game(*p, time_limit_1=time_limit, log=log)]
                if verbose:
                    print("{0[0]}{1} vs {0[1]}{2}".format(p,"*" if p[0]==winner else "", "*" if p[1]==winner else ""))
                wins[winner] += 1
                p = p[::-1]
    ranking = sorted(wins.keys(), key=lambda x:wins[x], reverse=True)
    for p in ranking:
        print("{}:{:.1%}".format(p, wins[p]/(games_per_pairing)/(len(players)-1)))
    return wins

if __name__ == '__main__':
    p0 = random_player("alice")
    p1 = random_player("bob")
    p2 = random_player("carol")
    hum = human_player("kaplan")
#     play_tournament(1000, p0, p1, p2, verbose=True, time_limit=10)
    play_game(p0, p1, True, True, 5)