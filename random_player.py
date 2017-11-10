'''
Created on Nov 9, 2017

@author: eliotkaplan
'''

from isola_game import isola_player
from random import choice

class random_player(isola_player):
    
    def __init__(self, name):
        super().__init__(name)
        
    def make_move(self):
        board = self.get_board()
        open_spaces = [(r,c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] == 0]
        players = [(r,c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] > 0]
        me = [c for c in players if board[c[0]][c[1]] == self.get_number()][0]
        movable = [(me[0]+i, me[1]+j) for i in range(-1,2) for j in range(-1,2) if (me[0]+i, me[1]+j) in open_spaces and (i != 0 or j != 0)]
        my_move = choice(movable)
        open_spaces.remove(my_move)
        open_spaces.append(me)
        my_remove = choice(open_spaces)
        return my_move, my_remove