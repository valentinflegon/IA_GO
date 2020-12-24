# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
import math
import random
from random import choice
from playerInterface import *


class myPlayer(PlayerInterface):

    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):
        return "############## Adil Rami  ##################"

    def getPlayerMove(self):
        move = alphaBeta(self,2,True)
        self._board.push(move)
        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 
       

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

################################################
# function heuristic: 
# add the number of stones captured by opponent 
# differece in the number of stones o the board
#
################################################

def heuristic(self):
    black_stones = 0
    white_stones = 0
    for r in range (0, self._board._BOARDSIZE): 
        for c in range (0, self._board._BOARDSIZE): 
            corr = [ r, c]
            x = self._board.flatten(corr)
            color = self._board.__getitem__(x)
            #empty si 0
            if color == 1: #black
                black_stones += 1 
            elif color == 2: #white
                white_stones += 1                 
    diff = black_stones - white_stones
    if self._board.next_player() == 1:
        return diff
    return -1*diff



################################################
# function alphaBeta( ... ): 
#  
################################################

def alphaBeta(b, depth, white):
    max_eval = -math.inf
    min_eval = math.inf
    alpha = -math.inf
    beta = math.inf
    best_move = []

    for i in b._board.legal_moves():
        b._board.push(i)
        eval = alphaBeta_rec(b, depth - 1, not white, alpha, beta)
        eval -= 0.00000001 * (100 - depth)
        b._board.pop()
        if white and max_eval <= eval:
            if max_eval == eval:
                best_move.append(i)
            else:
                best_move = [i]
                max_eval = eval
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        elif not white and min_eval >= eval:
            if min_eval == eval:
                best_move.append(i)
            else:
                best_move = [i]
                min_eval = eval
            beta = min(beta, eval)
            if alpha >= beta:
                break
    return random.choice(best_move)




################################################
# function alphaBeta( ... ): 
#  
################################################

def alphaBeta_rec(b, depth, white, alpha, beta):
    
    if depth == 0 or b._board.is_game_over():
        return heuristic(b)

    to_ret = None
    for i in b._board.legal_moves():
        if b._board.is_game_over():
            return 'PASS'
        b._board.push(i)
        eval = alphaBeta_rec(b, depth - 1, not white, alpha, beta)
        eval -= 0.00000001 * (100 - depth)  # valeur un peu magique pour faire varier le poids des
        b._board.pop()
        if to_ret is None:
            to_ret = eval
        if white:
            to_ret = max(to_ret, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        else:
            to_ret = min(to_ret, eval)
            beta = min(beta, eval)
            if alpha >= beta:
                break

    return to_ret

