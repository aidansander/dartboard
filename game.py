import tkinter as tk

    
class Player:
    def __init__(self, name):
        self.name = name
        self.hist = []

    def record_dart (self, dart):
        self.hist.append(dart)
    
    def undo_dart (self):
        self.hist.pop()

class Game:
    def __init__(self, playerlist):
        self.players = playerlist
        self.scorecounter = 0

    def record_dart(self, dart):
        self.players[(self.scorecounter//3)%len(self.players)].record_dart(dart)
        self.scorecounter += 1

    def undo_dart (self):
        if self.scorecounter>0:
            self.scorecounter -= 1
            self.players[(self.scorecounter//3)%len(self.players)].undo_dart()

    def update(self):
        for i in self.players:
            print (i.name, i.hist)

