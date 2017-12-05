'''
Created on Nov 9, 2017

@author: eliotkaplan
'''

from multiprocessing.pool import ThreadPool
import sys, os, time, datetime

# Disable
def block_print():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enable_print():
    sys.stdout = sys.__stdout__

class isola_game(object):
    
    def __init__(self, p1, p2, time_limit_1=None, time_limit_2=None):
        '''
        Create a new game between p1 and p2.
        time_limit is the amount of time that each player has to make all their moves.
        If you provide no time limits, time will be considered unlimited.
        If you provide one time limit, both players will get that amount of time
        If you provide two time limits, both players will start with different amounts of time
        '''
        self.done = False
        self.floor = [[True for _ in range(7)] for _ in range(7)]
        self.players = [p1, p2]
        if time_limit_1 == None and time_limit_2 == None:
            self.clock = [float('inf'), float('inf')]
        elif time_limit_1 == None:
            self.clock = [time_limit_2, time_limit_2]
        elif time_limit_2 == None:
            self.clock = [time_limit_1, time_limit_1]
        else:
            self.clock = [time_limit_1, time_limit_2]
        self.start_time = 0
        for p in self.players:
            p._game = self
        self.positions = [(0,3),(6,3)]
        
    def __str__(self):
        out = "  "
        out += " ".join([str(i) for i in range(len(self.floor))]) + "\n"
        for r in range(len(self.floor)):
            out += "{} ".format(r)
            for c in range(len(self.floor[r])):
                if (r,c) in self.positions:
                    out += str(self.positions.index((r,c))+1)
                else:
                    out += "_" if self.floor[r][c] else "X"
                out += " "
            out += "\n"
        for i in range(len(self.players)):
            t = "{:.2f}".format(self.clock[i]) if self.clock[i] < float('inf') else "∞"
            out += "{}: {} ({} seconds)\n".format(i+1, self.players[i], t)
        return out
    
    def play_turn(self, turn, f=None):
        ''' Plays out a single turn of the game '''
        if self.done: return
        try:
            if self.clock[turn] < float('inf'):
                pool = ThreadPool(processes=1)
                self.start_time = time.time()
                async_result = pool.apply_async(self.players[turn].make_move)
                move, wall = async_result.get(timeout=self.clock[turn])
                end = time.time()
                self.clock[turn] -= end-self.start_time
                pool.terminate()
            else:
                move, wall = self.players[turn].make_move()
            if move not in self.get_adjacent(self.positions[turn]):
                return (turn+1)%2
            self.positions[turn] = move
            if wall in self.positions or not self.floor[wall[0]][wall[1]]:
                return (turn+1)%2
            self.floor[wall[0]][wall[1]] = False
            if f:
                f.write("{0[0]}, {0[1]}, {1[0]}, {1[1]}\n".format(move, wall))
        except:
            print(sys.exc_info())
            return (turn+1)%2
        return -1
    
    def play_game(self, verbose=False, log=False):
        '''
        plays out a whole game.
        verbose determines whether or not the board gets printed at each step
        '''
        f = None
        if log:
            f = open("logs/{} vs {}_{}.csv".format(self.players[0], self.players[1], datetime.datetime.now()), "w")
        turn = 0
        for p in self.players:
            p.game_start()
        while True:
            if verbose:
                print("{}'s turn".format(self.players[turn].name))
                print(self)
            winner = self.play_turn(turn, f)
            if winner != -1:
                self.done = True
                if verbose:
                    print("{} wins!".format(self.players[winner].name))
                if f:
                    f.flush()
                    f.close()
                return winner
            else: turn = (turn+1)%2
        
    
    def get_board(self):
        '''
        returns the board as a 2D list of integers for player consumption, where each slot will be one of the following:
        -1 is a wall
        0 is an empty space
        1 is player 1's position
        2 is player 2's position
        '''
        out = [[0 if self.floor[r][c] else -1 for c in range(len(self.floor[r]))] for r in range(len(self.floor))]
        for i in range(len(self.positions)):
            out[self.positions[i][0]][self.positions[i][1]] = i+1
        return out
    
    def get_adjacent(self, coord):
        '''gets all spaces adjacent to a specific location, for legality checking'''
        poss = [(coord[0]+i, coord[1]+j) for i in range(-1,2) for j in range(-1,2) if i != 0 or j != 0]
        poss = [elem for elem in poss if 0 <= elem[0] < 7 and 0 <= elem[1] < 7 and self.floor[elem[0]][elem[1]]]
        return poss
    
class isola_player(object):
    
    def __init__(self, name):
        '''Creates a new isola player'''
        self.name = name
        self._game = None
        
    def __str__(self):
        return self.name
        
    def get_board(self):
        '''
        returns the board as a 2D list of integers for player consumption, where each slot will be one of the following:
        -1 is a wall
        0 is an empty space
        1 is player 1's position
        2 is player 2's position
        '''
        return self._game.get_board()
    
    def get_number(self):
        '''returns this isola player's number as they are represented in the board returned by get_board'''
        return self._game.players.index(self)+1
    
    def get_time(self):
        '''returns the amount of time left on this player's clock'''
        elapsed = time.time() - self._game.start_time
        return self._game.clock[self.get_number()-1] - elapsed
    
    def game_start(self):
        '''
        You need to override this function to reset your instance variables at the start of a game.
        '''
        pass
    
    def make_move(self):
        '''
        you need to override this function in your player to make moves.
        returns a pair of tuples
        the 0th returned tuple represents the coords of the space to which you'd like to move
        the 1th returned tuple represents the coords of the space you'd like to block
        both tuples are returned in (row, col) format
        '''
        return (0,0), (0,0)