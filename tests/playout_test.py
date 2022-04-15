from src.Player import Player
from src.Board import Board
from src.Shapes import *
from src.Blokus import Blokus

import random

board_size = 10

All_Shapes = ([I1(), I2(), I3(), I4(), I5(), 
              V3(), L4(), Z4(), O4(), L5(), 
              T5(), V5(), N(), Z5(), T4(), 
              P(), W(), U(), F(), X(), Y()])

All_Degrees = [0, 90, 180, 270]

All_Flip = ["None", "h"]

def Random_Player(player, game):
    """
    Algorithm for random play, stop search when it finds first possible move
    """
    shape_options = [p for p in player.pieces]
    
    while len(shape_options) > 0:
        piece = random.choice(shape_options)
        possibles = player.possible_moves([piece], game)
    
        # if there are not possible placements for that piece,
        # remove the piece from out list of pieces
        if possibles != []:
            return random.choice(possibles)
        
        else: shape_options.remove(piece)
    
    # if the while loop finishes without returning a possible move,
    # there must be no possible moves left, return None
    return None


a_player = Player("A", "Player_A", Random_Player)
b_player = Player("B", "Player_B", Random_Player)
c_player = Player("C", "Player_C", Random_Player)
d_player = Player("D", "Player_D", Random_Player)

standard_size = Board(board_size, board_size, "_")

randomblokus = Blokus([a_player, b_player,c_player,d_player], standard_size, All_Shapes[:5])

#winner = randomblokus.playout()

#print(winner)

import time
start = time.time()

winner = randomblokus.playout()

end = time.time()
print(end - start)

print(winner)


