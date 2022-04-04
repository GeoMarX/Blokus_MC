from src.Player import Player
from src.Board import Board
from src.Shapes import *
from src.Blokus import Blokus


piece1 = I5()
piece1.create(0, (0, 0))

piece2 = I1()
piece2.create(0, (9, 9))

def naive(player, game):
    return piece1

def naive2(player, game):
    return piece2

few = [I1(), I2(), I3(), I4(), I5()]

alice = Player("A", "Alice", naive)
bob = Player("B", "Bob", naive2)

bd = Board(10, 10, '_')
bd.print_board()


miniblokus = Blokus([alice, bob], bd, few)

 
print ("We should be on round zero: " + str(miniblokus.rounds))
 

miniblokus.play()
 

print ("The number of rounds should be incremented by one: " + str(miniblokus.rounds))
print 
print ("Alice's pieces should have the shape that was used in the move removed.")
print ([s.ID for s in alice.pieces])


print ("Recall that we are on this round: " + str(miniblokus.rounds))
 

miniblokus.play()
 

print ("The number of rounds should have been incremented by one: " + str(miniblokus.rounds))
 
print ("Alice's pieces should be the same as before!")
print ([s.ID for s in alice.pieces])
 
print ("Bob's pieces should have the shape that was used in the move removed.")
print ([s.ID for s in bob.pieces])
 
 
print("Let's see what the board looks like now: ")
 
miniblokus.board.print_board()
test = alice.possible_moves([P()], miniblokus)

for t in test:
    print (t.points)