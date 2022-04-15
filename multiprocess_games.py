import pickle
import os
import copy

from src.Player import Player
from src.Board import Board
from src.Shapes import *
from src.Blokus import Blokus
from math import sqrt, log


import datetime as dt
from multiprocessing import Process, current_process
import argparse
import sys

from agents import UCT_Player,RAVE_Player,Random_Player,PPA_Player



def gen_replays():

    n_replays = 10
    board_size = 5
    num_pieces = 4

    All_Shapes = ([I1(), I2(), I3(), I4(), I5(), 
              V3(), L4(), Z4(), O4(), L5(), 
              T5(), V5(), N(), Z5(), T4(), 
              P(), W(), U(), F(), X(), Y()])

    All_Degrees = [0, 90, 180, 270]

    All_Flip = ["None", "h"]


    for i in range(n_replays):


        print("Starting replay ",i+1)
        a_player = Player("A", "Player_A_PPA", PPA_Player,0)
        b_player = Player("B", "Player_B", Random_Player,1)
        c_player = Player("C", "Player_C", Random_Player,2)
        d_player = Player("D", "Player_D", Random_Player,3)

        standard_size = Board(board_size, board_size, "_")
        randomblokus = Blokus([a_player, b_player,c_player,d_player], standard_size, All_Shapes[:num_pieces])
        randomblokus.play()

        while randomblokus.winner() == "None":
            randomblokus.play()

        randomblokus.play()
        by_name = sorted(randomblokus.players, key = lambda player: player.score)
                

        
        name = "None"
        f = open("scores.txt", "a")
        for pl in by_name:
            f.write(f"Name = {pl.name}, Score = {pl.score} \n")
        f.write("__________________\n")
        f.close()
        
        
        print("Starting replay ",i+1,"-2")
        a_player = Player("A", "Player_A", Random_Player,0)
        b_player = Player("B", "Player_B_PPA", PPA_Player,1)
        c_player = Player("C", "Player_C", Random_Player,2)
        d_player = Player("D", "Player_D", Random_Player,3)

        standard_size = Board(board_size, board_size, "_")
        randomblokus = Blokus([a_player, b_player,c_player,d_player], standard_size, All_Shapes[:num_pieces])
        randomblokus.play()

        while randomblokus.winner() == "None":
            randomblokus.play()

        randomblokus.play()
        by_name = sorted(randomblokus.players, key = lambda player: player.score)
                


        f = open("scores.txt", "a")
        for pl in by_name:
            f.write(f"Name = {pl.name}, Score = {pl.score} \n")
        f.write("__________________\n")
        f.close()


        print("Starting replay ",i+1,"-3")
        a_player = Player("A", "Player_A", Random_Player,0)
        b_player = Player("B", "Player_B", Random_Player,1)
        c_player = Player("C", "Player_C_PPA", PPA_Player,2)
        d_player = Player("D", "Player_D", Random_Player,3)

        standard_size = Board(board_size, board_size, "_")
        randomblokus = Blokus([a_player, b_player,c_player,d_player], standard_size, All_Shapes[:num_pieces])
        randomblokus.play()

        while randomblokus.winner() == "None":
            randomblokus.play()

        randomblokus.play()
        by_name = sorted(randomblokus.players, key = lambda player: player.score)
                
       
        f = open("scores.txt", "a")
        for pl in by_name:
            f.write(f"Name = {pl.name}, Score = {pl.score} \n")
        f.write("__________________\n")
        f.close()

        
        print("Starting replay ",i+1,"-4")
        a_player = Player("A", "Player_A", Random_Player,0)
        b_player = Player("B", "Player_B", Random_Player,1)
        c_player = Player("C", "Player_C", Random_Player,2)
        d_player = Player("D", "Player_D_PPA", PPA_Player,3)

        standard_size = Board(board_size, board_size, "_")
        randomblokus = Blokus([a_player, b_player,c_player,d_player], standard_size, All_Shapes[:num_pieces])
        randomblokus.play()

        while randomblokus.winner() == "None":
            randomblokus.play()

        randomblokus.play()
        by_name = sorted(randomblokus.players, key = lambda player: player.score)
                
       
        f = open("scores.txt", "a")
        for pl in by_name:
            f.write(f"Name = {pl.name}, Score = {pl.score} \n")
        f.write("__________________\n")
        f.close()
        

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=5,
                        help='Number of processes')
    parser.add_argument('--n', type=int, default=2,
                        help='Number of replays/process ')

    args = parser.parse_args()
    worker_count = args.workers
    worker_pool = []
    for _ in range(worker_count):
        p = Process(target=gen_replays)
        p.start()
        worker_pool.append(p)
    for p in worker_pool:
        p.join()

