import tkinter as tk

import tkinter.font as tkFont
    
class Player:
    def __init__(self, name):
        self.name = name
        self.hist = []
        self.reset()

    def reset(self):
        #print ("player base reset")
        self.score = 0

    def record_dart (self, dart):
        self.hist.append(dart)
        self.score_dart(len(self.hist)-1)
    
    def undo_dart (self):
        self.hist.pop()
        self.reset()
        for i in range (0, len(self.hist)):
            self.score_dart(i)

    def score_dart(self, dartindex):
        dart = self.hist[dartindex]
        self.score += dart.multiplier * dart.number


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
        score = player.score
        return score
     
    def update(self):
        if self.frame:
            for i in range (0,self.playercount):
                self.playerlabels[i]['text'] = self.score_player(self.players[i])
            self.frame.update()

class CountDownPlayer (Player):

    def __init__(self, name, count_down, double_in=False, double_out=False):
        
        self.count_down = count_down
        self.double_in = double_in
        self.double_out = double_out
        super().__init__(name)
        
        #self.reset()
    
    def reset(self):
        #print ("countdownPlayer reset")
        self.is_in = not self.double_in
        self.is_out = not self.double_out
        self.roundscore = self.count_down
        self.score = self.count_down 

        
    def score_dart(self, dartindex):
        dart = self.hist[dartindex]
        #print ('countdownscore called')
        if dart.multiplier == 2:
            self.is_in = True
            
        if self.is_in:
            self.score -= dart.multiplier * dart.number
        if dartindex % 3 == 2:
            if self.score > 0:
                self.roundscore = self.score
            elif self.score < 0:
                self.score = self.roundscore
        if self.score == 0:
            if self.is_out:
                self.roundscore = self.score

            elif dartindex % 3 ==0 and dart.multiplier == 2:
                self.roundscore = self.score
            else:#TODO double check if double out requires double dart to win, i.e. does double 1, single 1, single 1, turn win on 4 points left, or does only double 2 win?
                self.score = self.roundscore
        
    





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

