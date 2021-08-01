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
    """Dartboard game class
    
    Parameters:
        playerlist: list of Players
        frame: tkframe to display score. May be None, in which case update does nothing
    
    """
    def __init__(self, playerlist, frame=None):
        self.players = playerlist
         
        self.dartcounter = 0
        self.playerlabels =[]
        self.frame = frame
        self.playercount = len(self.players)

        if frame:
            tablefont = tkFont.Font(family="Arial",size=28)
            for i in self.players:
                self.playerlabels.append(tk.Label(frame, text=i.name, bg='white', fg='black', font=tablefont))
            for i in self.playerlabels:
                i.pack(side=tk.TOP)

    def record_dart(self, dart):
        self.players[(self.dartcounter//3)%len(self.players)].record_dart(dart)
        self.dartcounter += 1

    def undo_dart (self):
        if self.dartcounter>0:
            self.dartcounter -= 1
            self.players[(self.dartcounter//3)%len(self.players)].undo_dart()
    
    def score_player(self, player):
        score = 0
        for i in player.hist:
            score += i.multiplier * i.number
        return score
     
    def update(self):
        if self.frame:
            for i in range (0,self.playercount):
                self.playerlabels[i]['text'] = self.score_player(self.players[i])
            self.frame.update()

class CountDownPlayer (Player):

    def __init__(self, name, count_down, double_in, double_out):
        
        self.count_down = count_down
        self.double_in = double_in
        self.double_out = double_out
        self.reset()
        self.is_in = not double_in
        self.is_out = not double_out
        self.score = count_down
        self.tempscore = count_down
        super().__init__(name)
    
    def reset(self):
        self.is_in = not self.double_in
        self.is_out = not self.double_out
    
    def record_dart(self, dart):
        super().record_dart(dart)
        score_dart(len(self.hist-1))
        
    def score_dart(dartindex):
        dart = self.hist[dartindex]
        if dart.multiplier == 2:
            self.is_in = True
            
        if self.is_in:
            self.tempscore -= dart.multiplier * dart.number
        if dartindex % 3 == 2:
            if self.tempscore > 0:
                self.score = self.tempscore
            elif self.tempscore < 0:
                self.tempscore = self.score
        if self.tempscore == 0:
            if self.is_out:
                self.score = self.tempscore

            elif dartindex % 3 ==0 and dart.multiplier == 2:
                self.score = self.tempscore
            else:#TODO double check if double out requires double dart to win, i.e. does double 1, single 1, single 1, turn win on 4 points left, or does only double 2 win?
                self.tempscore = self.score





#class CountDownGame (Game):
#    def __init__(self, playernames, frame, count_down, double_in, double_out):
#        self.count_down = count_down
#        self.double_in = double_in
#        self.double_out = double_out
#        
#        playerlist = [CountDownPlayer(i, count_down, double_in, double_out) for i in playernames]
#
#        super().__init__(playerlist, frame)
#
#    def score_player(self, player):
#        score = self.count_down
#        

