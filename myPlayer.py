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
        return "#####_Adémo_#####"

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
#   entrée: 
#   sortie: diff or -diff
#       
#       add the number of stones captured by opponent 
#       differece in the number of stones of the board
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
            if color == 1: #black
                black_stones += 1 
            elif color == 2: #white
                white_stones += 1                 
    diff = black_stones - white_stones
    if self._board.next_player() == 1:
        return [diff, black_stones, white_stones, color]
    return [-1*diff, black_stones, white_stones, color]



################################################
# fonction alphaBeta( ... ): 
#   entrée: board, une profondeur, un bool 
#   sortie: un move
#       
#       fonction qui donne pour valeur moins l'infini à alpha et plus l'infini à beta.
#    Ensuite on boucle sur tous les mouvements légaux et on applique ce mouvement à notre plateau, 
#    ce qui va nous donner un nouveau plateau de jeu.
#    On appelle récursivement sur AlphaBeta_rec avec le nouveau plateau et une profondeur en moins.
#    Ensuite en sortant de cet appel récursif on retire le coup joué et on cherche le meilleur coup
#    à jouer en fonction de l'heuristique retourné par AlphaBeta_rec. 
#    On peut couper si alpha est supérieur ou égal à beta, ce qui va faire gagner énormement de temps et de coup, 
#    chose que minimax ne fait pas.
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
# function alphaBeta_rec( ... ): 
#   entrée: un board, un profondeur, bool un alpha et un beta
#   sortie: un int qui provient de la fonction heuristic(b)
#        
#       Cette fonction est très similaire à AlphaBeta, mais elle vérifie si la profondeur
#    n'est pas égale à zéro ou si la partie n'est pas fini, dans ce cas on retourne un  appel la fonction
#    heuristique sur  le plateau tel qu'il est à ce moment-là. 
#    Ce qui va nous faire remonter dans nos appels récursifs.   
# 
################################################


def alphaBeta_rec(b, depth, white, alpha, beta):
    
    if depth == 0 or b._board.is_game_over():
        score, black, white, color = heuristic(b)
        if color == 2:
            if (black == 0 and white == 79):
                return -1
        if color == 1:
            if white == 0 and black == 79:
                return -1
        return heuristic(b)[0]
        
    to_ret = None
    for i in b._board.legal_moves():
        if b._board.is_game_over():
            return 'PASS'
        b._board.push(i)
        eval = alphaBeta_rec(b, depth - 1, not white, alpha, beta)
        eval -= 0.00000001 * (100 - depth) 
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

################################################
#   A partir de maintenant, toutes les fonctions sont nécessaires
#   pour une tentative d'heuristique plus performante.
#   Par manque de temps, nous n'avons pu affiner cette heuristique donc les pondérations 
#   des paramètres ne sont pas correctes.
#
#   Etait également en projet, une bibliothèque d'ouverture en fonction
#   des coups adverses.
#   
#   Nous voulions également coder des fonctions pour prendre en compte
#   les informations suivantes :
#       - y a t'il un oeil présent dans nos territoires
#       - est il possible de former un oeil ou plus
#       - est ce que la pierre jouée diminue notre territoire deja controlé
#       - reconnaitre des paternes commun, comme le shicho, le geta, atari sur la seconde ligne etc
################################################



################################################
# function sommeLibColor( ... ): 
#   entrée: un board ainsi que la couleur à évaluer
#   sortie: la somme des libertés de la couleur
#        
#       Cette fonction calcule la totalité des libertés
#       du joueur color.
# 
################################################

def sommeLibColor(b, color):
  sommelib = 0
  for x in range(b._board._BOARDSIZE):
    for y in range(b._board._BOARDSIZE):
      xycolor = b._board[Goban.Board.flatten((x,y))]
      if xycolor == color:
        sommelib += libPierre(b, (x,y))
  return sommelib


################################################
# function libPierre( ... ): 
#   entrée: un board, les coordonées de la pierre à évaluer
#   sortie: un int, représentant les libertés de la pierre de coordonées coord
#        
#       Cette fonction compte le nombre de liberté de la pierre à la position coord.
#       Est utilisée pour compter les liertés d'une chaine.
# 
################################################
def libPierre(b, coord):
  lib = 0
  (x,y) = coord
  if x==0 and y==0:
    if b._board[Goban.Board.flatten((x+1,y))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x,y+1))]==0:
      lib += 1
  elif x==8 and y==8:
    if b._board[Goban.Board.flatten((x-1,y))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x,y-1))]==0:
      lib += 1
  elif x==8 and y==0:
    if b._board[Goban.Board.flatten((x-1,y))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x,y+1))]==0:
      lib += 1
  elif x==0 and y==8:
    if b._board[Goban.Board.flatten((x+1,y))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x,y-1))]==0:
      lib += 1
  elif y==0:
    if b._board[Goban.Board.flatten((x,y+1))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x-1,y))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x+1,y))]==0:
      lib += 1
  elif x==0:
    if b._board[Goban.Board.flatten((x,y+1))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x,y-1))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x+1,y))]==0:
      lib += 1
  elif y==8:
    if b._board[Goban.Board.flatten((x,y-1))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x-1,y))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x+1,y))]==0:
      lib += 1
  elif x==8:
    if b._board[Goban.Board.flatten((x,y+1))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x-1,y))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x,y-1))]==0:
      lib += 1
  elif x>0 and x<8 and y>0 and y<8:
    if b._board[Goban.Board.flatten((x,y+1))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x,y-1))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x+1,y))]==0:
      lib += 1
    if b._board[Goban.Board.flatten((x-1,y))]==0:
      lib += 1
  return lib



################################################
# function libChaine( ... ): 
#   entrée: un board, une liste de position
#   sortie: un int représentant les libertés d'une chaine
#        
#       Cette fonctione utilise libPierre(...) pour calculer les libertés de 
#       la chaine représentée par la liste de position en entrée.
# 
################################################

def libChaine(b, chaine):
  lib = 0
  for (x,y) in chaine :
    lib += libPierre(b,(x,y))
  return lib




################################################
#       Cette fonction est utilitaire, pour fournir une copie des
#       positions occupées.
# 
################################################

def copyColorBoard(b):
  copy = []
  for i in range(81):
    copy.append(b._board[i])
  return copy


################################################
# function cutChaine( ... ): 
#   entrée: un board
#   sortie: une liste de listes représentants les chaines
#        
#       Cette fonction permet de calculer toutes les chaines du Goban.   
# 
################################################

def cutChaine(b):
  bcolor = copyColorBoard(b)
  listechaine = []
  for i in range(80):
    if bcolor[i] != 0:
      chaine = []
      (x,y) = b._board.unflatten(i)
      color = bcolor[i]
      constChaine(bcolor, b, color, (x,y), chaine)
      listechaine.append(chaine)
  return listechaine



################################################
# function cutChaineColor( ... ): 
#   entrée: un board, un int représentant une couleur
#   sortie: une liste de listes représentants les chaines
#        
#       Cette fonction est très similaire à cuChaine(...), elle permet de récuperer
#       seulement les chaines de la couleur passées en paramètres.
# 
################################################


def cutChaineColor(b, color):
  bcolor = copyColorBoard(b)
  listechaine = []
  for i in range(80):
    if bcolor[i] == color:
      chaine = []
      (x,y) = b._board.unflatten(i)
      constChaine(bcolor, b, color, (x,y), chaine)
      listechaine.append(chaine)
  return listechaine



################################################
# function constChaine( ... ): 
#   entrée: une liste d'entier, un board, une couleur, une position, une liste de position
#   sortie: pas de sortie, modifie la liste de position en entree
#        
#       Cette fonction récursive construit une chaine respectant la couleur color
#       et la stocke dans chaine.
# 
################################################

def constChaine(bcolor, b, color, pos, chaine):
  (x,y) = pos
  n = b._board.flatten(pos) 
  if n>80 or bcolor[n] != color:
    return
  else:
    chaine.append(pos)
    bcolor[n] = 0
    if x==0 and y==0:
      constChaine(bcolor, b, color, (x,y+1), chaine)
      constChaine(bcolor, b, color, (x+1,y), chaine)
    if x==8 and y==8:
      constChaine(bcolor, b, color, (x,y-1), chaine)
      constChaine(bcolor, b, color, (x-1,y), chaine)
    if x==8 and y==0:
      constChaine(bcolor, b, color, (x-1,y), chaine)
      constChaine(bcolor, b, color, (x,y+1), chaine)
    if x==0 and y==8:
      constChaine(bcolor, b, color, (x+1,y), chaine)
      constChaine(bcolor, b, color, (x,y-1), chaine)
    if y==0:
      constChaine(bcolor, b, color, (x,y+1), chaine)
      constChaine(bcolor, b, color, (x+1,y), chaine)
      constChaine(bcolor, b, color, (x-1,y), chaine)
    if x==0:
      constChaine(bcolor, b, color, (x,y-1), chaine)
      constChaine(bcolor, b, color, (x+1,y), chaine)
      constChaine(bcolor, b, color, (x,y+1), chaine)
    if y==8:
      constChaine(bcolor, b, color, (x+1,y), chaine)
      constChaine(bcolor, b, color, (x,y-1), chaine)
      constChaine(bcolor, b, color, (x-1,y), chaine)
    if x==8:
      constChaine(bcolor, b, color, (x,y-1), chaine)
      constChaine(bcolor, b, color, (x-1,y), chaine)
      constChaine(bcolor, b, color, (x,y+1), chaine)
    if x>0 and x<8 and y>0 and y<8:
      constChaine(bcolor, b, color, (x+1,y), chaine)
      constChaine(bcolor, b, color, (x,y+1), chaine)
      constChaine(bcolor, b, color, (x-1,y), chaine)
      constChaine(bcolor, b, color, (x,y-1), chaine)
        
  


################################################
# function isAtariChaine( ... ): 
#   entrée: un board, une liste de position
#   sortie: un Booleen
#        
#       Cette fonction calcule les liertés d'un chaine
#       et renvoie vrai si la chaine est en position atari.   
# 
################################################

def isAtariChaine(b, chaine):
  if libChaine(b, chaine)==1:
    return True
  return False


################################################
# function nbAtari( ... ): 
#   entrée: un board
#   sortie: un int
#        
#       Cette fonction calcule les libertés d'un chaine
#       le nombre de chaine en Atari sur le Goban.
# 
################################################
 
def nbAtari(b):
  nbAtari = 0
  listechaine = cutChaine(b)
  for chaine in listechaine:
    if isAtariChaine(b, chaine):
      nbAtari += 1
  return nbAtari


################################################
# function nbAtariColor( ... ): 
#   entrée: un board, un int representant une couleur
#   sortie: un int
#        
#       Cette fonction est une variante de nbAtari
#       et calcule le nombre de chaine en Atari sur le Goban
#       d'une couleur donnée.
# 
################################################

def nbAtariColor(b, color):
  nbAtari = 0
  listechaine = cutChaineColor(b,color)
  for chaine in listechaine:
    if isAtariChaine(b, chaine):
      nbAtari += 1
  return nbAtari


################################################
# function heuristique2( ... ): 
#   entrée: un board
#   sortie: un int representant le score du plateau
#        
#       Cette fonction tente une évaluation du plateau
#       en se basant sur le nombre de chaine en atari, ami et ennemi, 
#       ainsi que sur les libertés totales ami et ennemi et l'heuristique
#       évaluant la difference de pierre sur le Goban. Les poids ne sont pas optimisés.
# 
################################################

def heuristique2(b):
  if b._board.next_player() == 2:
    mycolor = 1
    encolor = 2
  if b._board.next_player() == 1:
    mycolor = 2
    encolor = 1
  score = 0
  score += 0.5*nbAtariColor(b, encolor)
  score -= 0.5*nbAtariColor(b, mycolor)
  h1 = heuristic(b)[0]
  score += (0.25)*h1
  score += (0.25)*(sommeLibColor(b, mycolor))
  score -= (0.25)*(sommeLibColor(b, encolor))
  return score  

