import tkinter as tk
#import cwiid as cw
import time
import math
from enum import IntEnum
import keyboard


from dart import Dart

from game import Player
from game import Game
from game import CountDownPlayer
from board import Board
from button import Button
from keyboard_input import KeyboardInput

root = tk.Tk()
board = Board()
board.create_board(root)

num_players = 2
players = [CountDownPlayer('Player' + str(i+1), 301) for i in range(num_players)]

frame = tk.Frame(root)
frame.pack(side=tk.LEFT)
game = Game(players, frame) 

board.update()
root.update() 

key_reader = KeyboardInput()

while True:

    key_reader.update_button_bits()
    if key_reader.button_bits:
        if key_reader.button_held("left"):
            board.move_left() 
        elif key_reader.button_held("right"):
            board.move_right() 
        if key_reader.button_held("up"):
            board.move_up()
        elif key_reader.button_held("down"):
            board.move_down()
        if key_reader.button_clicked("enter"):
            game.record_dart(board.get_selected())
            game.update()
        if key_reader.button_clicked("backspace"):
            game.undo_dart()
            game.update()
        board.update()
    root.update() 