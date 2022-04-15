from src.Player import Player
from src.Board import Board
from src.Shapes import *
from src.Blokus import Blokus
from math import sqrt, log

import random
import copy

board_size = 5
num_pieces = 4

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


def RAVE_Player(player,game):
    
    n = 100
    Table = {}  

    def addAMAF (game):
        MaxLegalMoves = 1000
        MaxCodeLegalMoves = 100000
        nplayouts = [0.0 for x in range (MaxLegalMoves)]
        nwins = [[0.0,0.0,0.0,0.0] for x in range (MaxLegalMoves)]
        nplayoutsAMAF = [0.0 for x in range (MaxCodeLegalMoves)]
        nwinsAMAF = [[0.0,0.0,0.0,0.0] for x in range (MaxCodeLegalMoves)]
        Table [game.h] = [0, nplayouts, nwins, nplayoutsAMAF, nwinsAMAF]

    def updateAMAF (t, played, res):
        for i in range (len (played)):
            code = played [i]
            seen = False
            for j in range (i):
                if played [j] == code:
                    seen = True
            if not seen:
                t [3] [code] += 1
                t [4] [code] [res] += 1

    def look (game):
        return Table.get (game.h, None)
    
    def RAVE (game, played):
        if game.winner() != "None":
            return game.winner().idx
        
        t = look (game)
        if t != None:
            bestValue = -1000000.0
            best = 0

            current = game.players[0]
            shape_options = [p for p in current.pieces]
            moves = current.possible_moves(shape_options, game)
            if len(moves) != 0:
                bestcode = game.get_hash(moves [0], current.idx)
                bestcode = int(str(bestcode)[:5])
                
            for i in range (0, len (moves)):
                val = 1000000.0
                
                if len(moves) != 0:
                    code = game.get_hash(moves [i], current.idx)
                    code = int(str(code)[:5])
                
                if t [3] [code] > 0:
                    beta = t [3] [code] / (t [1] [i] + t [3] [code] + 1e-5 * t [1] [i] * t [3] [code])
                    Q = 1
                    if t [1] [i] > 0:
                        Q = t[2] [i] [current.idx] / t [1] [i]
                    AMAF = t [4] [code] [current.idx] / t [3] [code]
                    val = (1.0 - beta) * Q + beta * AMAF
                if val > bestValue:
                    bestValue = val
                    best = i
                    bestcode = code

            if len (moves) == 0 :
                #addAMAF(game)
                return game.playout().idx
            else:
                game.play_move (moves[best])

            res = RAVE (game, played)

            t [0] += 1
            t [1] [best] += 1
            t [2] [best] [res] += 1
            played.insert (0, bestcode)
            for k in range (len (played)):
                code = played [k]
                seen = False
                for j in range (k):
                    if played [j] == code:
                        seen = True
                if not seen:
                    t [3] [code] += 1
                    t [4] [code] [res] += 1
            return res
        else:
            addAMAF (game)
            return game.playoutAMAF(played).idx
    
    def BestMoveRAVE (game, n):
        global Table
        Table = {}
        for i in range (n):
            b1 = copy.deepcopy (game)
            res = RAVE (b1, [])
        t = look (game)

        current = game.players[0]
        shape_options = [p for p in current.pieces]
        moves = current.possible_moves(shape_options, game)
        
        if len(moves) == 0:
            return None
        else:
            best = moves [0]
            bestValue = t [1] [0]
            for i in range (1, len(moves)):
                if (t [1] [i] > bestValue):
                    bestValue = t [1] [i]
                    best = moves [i]
            return best
    
    return BestMoveRAVE(game,n)

    
a_player = Player("A", "Player_A", RAVE_Player,0)
b_player = Player("B", "Player_B", Random_Player,1)
c_player = Player("C", "Player_C", Random_Player,2)
d_player = Player("D", "Player_D", Random_Player,3)

standard_size = Board(board_size, board_size, "_")

randomblokus = Blokus([a_player, b_player,c_player,d_player], standard_size, All_Shapes[:num_pieces])

randomblokus.play()
randomblokus.board.print_board(num = randomblokus.rounds, fancy = False)

while randomblokus.winner() == "None":
    randomblokus.play()
    randomblokus.board.print_board(num = randomblokus.rounds, fancy = False)

print("") 
randomblokus.board.print_board()
print("")
randomblokus.play()

print("The final scores are...")

by_name = sorted(randomblokus.players, key = lambda player: player.name)

for p in by_name:
    print (p.name + " : " + str(p.score))
