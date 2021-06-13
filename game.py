import tkinter as tk

import tkinter.font as tkFont
    
class Player:
    def __init__(self, name):
        self.name = name
        self.hist = []

    def record_dart (self, dart):
        self.hist.append(dart)
    
    def undo_dart (self):
        self.hist.pop()

class Game:
    
    def __init__(self, playerlist, frame):
        self.players = playerlist
        self.scorecounter = 0
        self.playerlabels =[]
        self.frame = frame
        self.playercount = len(self.players)

        tablefont = tkFont.Font(family="Arial",size=28)

        for i in self.players:
            self.playerlabels.append(tk.Label(frame, text=i.name, bg='white', fg='black', font=tablefont))
        for i in self.playerlabels:
            i.pack(side=tk.TOP)

    def record_dart(self, dart):
        self.players[(self.scorecounter//3)%len(self.players)].record_dart(dart)
        self.scorecounter += 1

    def undo_dart (self):
        if self.scorecounter>0:
            self.scorecounter -= 1
            self.players[(self.scorecounter//3)%len(self.players)].undo_dart()
    
    def score_player(self, player):
        score = 0
        for i in player.hist:
            score += i.multiplier * i.number
        return score

    
    def update(self):
        for i in range (0,self.playercount) :
            self.playerlabels[i]['text'] = self.score_player(self.players[i])
        self.frame.update()
