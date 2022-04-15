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

def All_moves(player, game):
    """
    Function that returns all possible moves
    """
    shape_options = [p for p in player.pieces]
    moves = player.possible_moves(shape_options, game) 
    
    if moves is None:
        return None
    print(len(moves))
    if len(moves) == 0:
        return None
    return random.choice(moves)

def UCT_Player(player,game):
    n = 100

    Table = {}
    
    def add (game):
        MaxLegalMoves = 1000
        nplayouts = [0.0 for x in range (MaxLegalMoves)]
        nwins = [[0.0,0.0,0.0,0.0] for x in range (MaxLegalMoves)]
        Table [game.h] = [0, nplayouts, nwins]
    
    def look (game):
        return Table.get (game.h, None)
    
    def UCT (game):
        if game.winner() != "None":
            return game.winner().idx
        t = look (game)
        
        if t != None:
            bestValue = -1000000.0
            best = 0
            
            #moves = game.legalMoves()
            current = game.players[0]
            shape_options = [p for p in current.pieces]
            moves = current.possible_moves(shape_options, game) 

            for i in range (0, len (moves)):
                val = 1000000.0
                if t [1] [i] > 0:
                    Q = t[2][i][current.idx] / t[1][i]
                    val = Q + 0.4 * sqrt (log(t[0]) / t[1][i])
                if val > bestValue:
                    bestValue = val
                    best = i


            if len (moves) == 0 :
                return game.playout().idx

            else:
                game.play_move (moves[best])
            
            res = UCT (game)

            t [0] += 1
            t [1] [best] += 1
            t [2] [best][res] += 1
            return res
        else:
            add (game)
            return game.playout().idx
    
    def BestMoveUCT (game, n):
        global Table
        Table = {}
        for i in range (n):
            b1 = copy.deepcopy (game)
            res = UCT (b1)
        t = look (game)
        
        current = game.players[0]
        shape_options = [p for p in current.pieces]
        moves = current.possible_moves(shape_options, game)

        if len(moves) == 0:
            return None
        else:

            best = moves [0]
            bestValue = t [1] [0]
            print(t[2][:20])
            for i in range (1, len(moves)):
                if (t [1] [i] > bestValue):
                    bestValue = t [1] [i]
                    best = moves [i]
            return best
        
    return BestMoveUCT(game,n)

def PPA_Player(player,game):
    n = 100
    Table = {}

    def add (game):
        MaxLegalMoves = 1000
        nplayouts = [0.0 for x in range (MaxLegalMoves)]
        nwins = [[0.0,0.0,0.0,0.0] for x in range (MaxLegalMoves)]
        Table [game.h] = [0, nplayouts, nwins]
    
    def look (game):
        return Table.get (game.h, None)
    
    def adapt (game, winner, state, policy):
        polp = copy.deepcopy (policy)
        alpha = 0.32
        while game.winner() == "None":
            current = game.players[0]
            shape_options = [p for p in current.pieces]
            l = current.possible_moves(shape_options, game) 
            
            move = state.history [len(game.history)]
            # save all played moves in parameter of state 
            if current.idx == winner:
                z = 0
                for i in range (len (l)):
                    z = z + math.exp (policy.get (game.get_hash(l[i], current.idx),0))
                polp[game.get_hash(move, current.idx)] = polp.get(game.get_hash(move, current.idx),0) + alpha
                for i in range (len (l)):
                    proba = math.exp (policy.get (game.get_hash(l[i], current.idx),0)) / z
                    polp[game.get_hash(l[i], current.idx)] = polp.get(game.get_hash(l[i], current.idx),0) - alpha * proba
            
            # print(state.history)
            # print(game.history)
            # print(current.name)
            game.play_move(move)
        return polp

    def PPAF (game, policy):
        
        if game.winner() != "None":
            return game.winner().idx
        
        t = look (game)
        
        if t != None:
            bestValue = -1000000.0
            best = 0
            
            current = game.players[0]
            shape_options = [p for p in current.pieces]
            moves = current.possible_moves(shape_options, game) 
            for i in range (0, len (moves)):
                val = 1000000.0
                if t [1] [i] > 0:
                    Q = t[2][i][current.idx] / t[1][i]
                    val = Q + 0.4 * sqrt (log(t[0]) / t[1][i])
                if val > bestValue:
                    bestValue = val
                    best = i
            if len (moves) == 0 :
                return game.playout_PPA(policy).idx
            else:
                game.play_move (moves[best])
            
            res = PPAF (game, policy)

            t [0] += 1
            t [1] [best] += 1
            t [2] [best][res] += 1
            return res
        else:
            add (game)
            return game.playout_PPA(policy).idx

    def BestMovePPAF (game, n):
        Table = {}
        policy = {}
        for i in range (n):
            print("playout",i,flush=True)
            b1 = copy.deepcopy (game)
            res = PPAF (b1, policy)
            b2 = copy.deepcopy (game)
            policy = adapt (b2, res, b1, policy)             
        
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
    
    return BestMovePPAF(game,n)

a_player = Player("A", "Player_A", PPA_Player,0)
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
