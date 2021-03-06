from src.Game import Game

class Blokus(Game):
    """
    A class that takes a list of players, e.g. ['A','B','C'],
    and a board and plays moves, keeping track of the number
    of rounds that have been played.
    """        
    def winner(self):
        """
        Checks the conditions of the game
        to see if the game has been won yet
        and returns "None" if the game has
        not been won, and the name of the
        player if it has been won.
        """
        moves = [p.possible_moves(p.pieces, self) for p in self.players]
        if False in [mv == [] for mv in moves]:
            return("None")
        else:
            cand = [(p.score, p.name,p) for p in self.players]
            return(sorted(cand, reverse=True)[0][2])
    def valid_move(self, player, move):
        """
        Uses functions from the board to see whether
        a player's proposed move is valid.
        """
        if self.rounds < len(self.players):
            if ((False in [(self.board).in_bounds(pt) for pt in move])
            or (self.board).overlap(move)
            or not (True in [(pt in player.corners) for pt in move])):
                return(False)
            else: return(True)
        
        elif ((False in [(self.board).in_bounds(pt) for pt in move])
        or (self.board).overlap(move) 
        or (self.board).adj(player, move)  
        or not (self.board).corner(player, move)):
            return(False)
        
        else: return(True)