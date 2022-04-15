from src.Player import Player
from src.Board import Board
from src.Shapes import *
from src.Blokus import Blokus
from math import sqrt, log
import numpy as np
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





def nested_player(player, game):
    depth = 2

    table = {} #table where we stock our games to avoir repeating

    def add (game):
        MaxLegalMoves = 1000
        nplayouts = [0.0 for x in range (MaxLegalMoves)]
        nwins = [[0.0,0.0,0.0,0.0] for x in range (MaxLegalMoves)]
        Table [game.h] = [0, nplayouts, nwins]

    def look (game):
        return Table.get (game.h, None)

    def nested(game, depth):
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
                add (game)
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

def UCT (game):
    Table = {}
    def add (game):
        MaxLegalMoves = 1000
        nplayouts = [0.0 for x in range (MaxLegalMoves)]
        nwins = [[0.0,0.0,0.0,0.0] for x in range (MaxLegalMoves)]
        Table [game.h] = [0, nplayouts, nwins]

    def look (game):
        return Table.get (game.h, None)

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
                add (game)
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


def adapt(winner, game, player, playout, policy):
    alpha = 1
    polp = copy.deepcopy(policy)
    for m in playout:
        if winner.idx == player.idx:
            polp[m] += alpha
        z=0
        current = game.players[0]
        shape_options = [p for p in current.pieces]
        moves = current.possible_moves(shape_options, game) 
        for poss_m in moves:
            z += np.exp(policy.get(poss_m))
        for poss_m in moves:
            polp[m] -= alpha*np.exp(policy.get(poss_m))/z
        (game.board).update(current, m.points)
        # let the player update itself accordingly
        current.update_player(m, game.board)
        # remove the piece that was played from the player
        current.remove_piece(m)
        # place the player at the back of the queue
        game.history.append(m)
        first = (game.players).pop(0)
        game.players = game.players + [first]
        # increment the number of rounds just played
        game.rounds += 1
    policy = polp

def PPA_playout(game,policy):
    """
    Policy here is a dictionnary with moves in keys and smth in values
    """
    while True:

        if game.winner() != "None":
                return game.winner().idx
        
        z = 0
        current = game.players[0]
        shape_options = [p for p in current.pieces]
        moves = current.possible_moves(shape_options, game) 
        for m in moves:
            if m not in policy:
                policy[m] = 0
            z += np.exp(policy.get(m,0))
        move = random.choices(list(policy.keys()), weights=policy.values())
        # update the board with the move
        (game.board).update(current, move.points)
        # let the player update itself accordingly
        current.update_player(move, game.board)
        # remove the piece that was played from the player
        current.remove_piece(move)
        # place the player at the back of the queue
        first = (game.players).pop(0)
        game.players = game.players + [first]
        # increment the number of rounds just played
        game.rounds += 1


def PPA_Player(player,game):
    n_playouts = 100
    policy = {}
    current = game.players[0]
    shape_options = [p for p in current.pieces]
    moves = current.possible_moves(shape_options, game) 
    for m in moves:
        policy[m] = 0
    for i in range(n_playouts):
        current_g = copy.deepcopy(game)
        winner = UCT(current_g)
        current_g1 = copy.deepcopy(game)
        adapt(winner, current_g1, player, current_g.playout, policy)

    return max(policy, key=policy.get)





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
                add (game)
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
            #print("Starting sim num",i)
            b1 = copy.deepcopy (game)
            res = UCT (b1)
        t = look (game)
        
        current = game.players[0]
        shape_options = [p for p in current.pieces]
        moves = current.possible_moves(shape_options, game)
        #print(moves)
        if len(moves) == 0:
            return None
        else:

            best = moves [0]
            bestValue = t [1] [0]
            print(t[1])
            for i in range (1, len(moves)):
                if (t [1] [i] > bestValue):
                    bestValue = t [1] [i]
                    best = moves [i]
            return best
        
    return BestMoveUCT(game,n)



    
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
