'''
Created on Nov 10, 2017

@author: eliotkaplan
'''
from isola_game import isola_player

class human_player(isola_player):
    '''
    An isola player controlled by a human. Totally illegal in the actual competition, but 
    a good way to test that your bot plays well. You'll probably want to set the time limit
    to a high value or to infinity, because the clock is running while you consider your move.
    '''

    def __init__(self, name):
        super().__init__(name)
        
    def make_move(self):
        print("MOVEMENT")
        row = int(input("{}, choose a row: ".format(self.name)))
        col = int(input("{}, choose a col: ".format(self.name)))
        move = (row, col)
        print("WALL PLACEMENT")
        row = int(input("{}, choose a row: ".format(self.name)))
        col = int(input("{}, choose a col: ".format(self.name)))
        wall = (row, col)
        return move, wall