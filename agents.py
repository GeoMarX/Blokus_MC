import copy
from math import sqrt, log
import random

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
            if current.idx == winner:
                z = 0
                for i in range (len (l)):
                    z = z + math.exp (policy.get (game.get_hash(l[i], current.idx),0))
                polp[game.get_hash(move, current.idx)] = polp.get(game.get_hash(move, current.idx),0) + alpha
                for i in range (len (l)):
                    proba = math.exp (policy.get (game.get_hash(l[i], current.idx),0)) / z
                    polp[game.get_hash(l[i], current.idx)] = polp.get(game.get_hash(l[i], current.idx),0) - alpha * proba
            
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