import tkinter as tk
import cwiid as cw
import time
import math
import tkinter.font as tkFont
from enum import IntEnum

from dart import Dart

from game import Player
from game import Game


class Button:
    
    def __init__(self, buttonmask, buttondelay = 0, holddelay = 0):
        self.buttonmask = buttonmask
        self.lastclickedtime = 0
        self.lastheldtime = 0
        self.buttondelay = buttondelay
        self.holddelay = holddelay
        assert self.holddelay <= self.buttondelay
        
    def button_clicked(self,buttons, lastbuttons, nowtime):    
        if (buttons & self.buttonmask) and not (lastbuttons & self.buttonmask):
            self.lastclickedtime = nowtime
            return (True, 0)
        elif (buttons & self.buttonmask):
            return (False, nowtime - self.lastclickedtime)
        return (False, 0)

    def button_held (self, buttons, lastbuttons, nowtime):
        (clicked , heldtime) = self.button_clicked(buttons, lastbuttons, nowtime)
        if clicked or (nowtime - self.lastheldtime >= self.holddelay and  heldtime >= self.buttondelay):
            self.lastheldtime = nowtime
            return True
        return False

def connect_wiimote():
    for i in range (10):
        print ('press 1 and 2 on wiimote')
        try:
            wii = cw.Wiimote()
            print ("wiimote connected!!!!!!!")
            return wii
        except RuntimeError:
            pass
    print ("wiimote timed out")

class Arcy(IntEnum):
    MISS = 0
    DOUBLE_ARC = 1
    SINGLE_ARC_OUTER = 2
    TRIPLE_ARC  = 3
    SINGLE_ARC_INNER = 4
    BULL  = 5
    DOUBLE_BULL  = 6

class Board:
    numbers = [13,4,18,1,20,5,12,9,14,11,8,16,7,19,3,17,2,15,10,6] 

    def __init__(self):
        self.arcx = 0
        self.arcy = 0
        self.next_arcx = 0
        self.next_arcy = 0

    def move_left(self):
        self.next_arcx = (self.next_arcx + 1) % len(self.arcs[self.arcy])
    
    def move_right(self):
        self.next_arcx = (self.next_arcx - 1) % len(self.arcs[self.arcy])
    
    def move_up(self):
        if self.next_arcy > 0:
            self.next_arcy -= 1
    
    def move_down(self):
        if self.next_arcy < len(self.arcs) - 1:
            self.next_arcy += 1
    
    def update(self):
        self.canvas.itemconfigure(self.arcs[self.arcy][self.arcx], state='normal')
        self.arcx = self.next_arcx
        self.arcy = self.next_arcy
        self.canvas.itemconfigure(self.arcs[self.arcy][self.arcx], state='disabled')

        print ("selection=", self.get_selected())

    def create_text(self, center, diameter):
        radius = diameter/2
        font = tkFont.Font(size=18,weight='bold')
        for i in range (0, 20):
            angle_deg = i * 18 + 18 
            angle_rad = math.radians(angle_deg)
            if i<10:
                angle_txt = 270 + angle_deg 
            elif i==19:
                angle_txt = 0
            else:
                angle_txt = 90 + angle_deg
            self.canvas.create_text(center[0]+math.cos(angle_rad)*(radius),
                               center[1]-math.sin(angle_rad)*(radius), 
                               text=self.numbers[i],
                               angle=angle_txt,
                               font=font) 
   
    def create_arcs(self, center, diameter, color0, color1, highlightcolor):
        arcs = []
        radius = diameter/2
        coord = (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)
        for i in range (0, 20):
            color = color0 if i%2 else color1
            arcs.append(self.canvas.create_arc(coord, start=i*18+9, extent=18, fill=color, disabledfill=highlightcolor))
        return arcs

    def create_circle(self, center, diameter, color, highlightcolor):
        
        radius = diameter/2
        coord = (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)
        circle = self.canvas.create_oval(coord, fill=color, disabledfill=highlightcolor)
        return 20*[circle]


    def create_board(self, root, width=900, height=800, border=70, highlightcolor='gold'):
       #TODO get some anti-aliasing in here 
        self.canvas = tk.Canvas(root, bg='white', width=width, height=height)
        diameter = height - border
        center = (width/2,  height/2)
        self.arcs = []
        miss =  self.canvas.create_text(center[0]+diameter/2 + 10, center[1]-diameter/2, text='miss', font=tkFont.Font(size=18,weight='bold'), disabledfill=highlightcolor)
        print (self.canvas.bbox(miss))
        self.arcs.append(20*[miss])
        self.arcs.append(self.create_arcs(center, diameter, 'green', 'red', highlightcolor))  
        self.arcs.append(self.create_arcs(center, .90*diameter, 'white', 'black', highlightcolor))
        self.arcs.append(self.create_arcs(center, .55*diameter, 'green', 'red', highlightcolor))
        self.arcs.append(self.create_arcs(center, .45*diameter, 'white', 'black', highlightcolor))
        self.arcs.append(self.create_circle(center, .07*diameter, 'green', highlightcolor)) # bull
        self.arcs.append(self.create_circle(center, .03*diameter, 'red', highlightcolor)) # double-bull
        self.create_text(center, 1.05*diameter)
        self.canvas.pack(side=tk.LEFT) #reality is often dissapointing

        assert len(self.arcs) - 1 == Arcy.DOUBLE_BULL

    def get_selected(self):

        number = self.numbers[self.arcx]
        if self.arcy == Arcy.MISS:
            multiplier = 0
            number = 0
        elif self.arcy == Arcy.DOUBLE_ARC:
            multiplier = 2
        elif self.arcy in (Arcy.SINGLE_ARC_OUTER, Arcy.SINGLE_ARC_INNER):
            multiplier = 1
        elif self.arcy == Arcy.TRIPLE_ARC:
            multiplier = 3
        elif self.arcy == Arcy.BULL:
            multiplier = 1
            number = 25
        elif self.arcy == Arcy.DOUBLE_BULL:
            multiplier = 2
            number = 25

        return Dart(multiplier, number)

root = tk.Tk()
board = Board()
board.create_board(root)

num_players = 2
players = [Player('Player' + str(i+1)) for i in range(num_players)]

frame = tk.Frame(root)
frame.pack(side=tk.LEFT)
game = Game(players, frame) 

board.update()
root.update() 
        
wii = connect_wiimote()
wii.rpt_mode = cw.RPT_BTN

button_delay = 0.4
hold_delay = .1

    
left_button = Button(cw.BTN_LEFT, button_delay, hold_delay)
right_button = Button(cw.BTN_RIGHT, button_delay, hold_delay)
up_button = Button(cw.BTN_UP, button_delay, hold_delay)
down_button = Button(cw.BTN_DOWN, button_delay, hold_delay)
select_button = Button(cw.BTN_A, button_delay, hold_delay)
back_button = Button(cw.BTN_B, button_delay, hold_delay)



old_buttons = 0
wii.led = 1
while True:
    buttons = wii.state['buttons']
    total_delay=0
    nowtime = time.time()
     
    if (buttons):
        if left_button.button_held(buttons, old_buttons, nowtime):
            board.move_left() 
        elif right_button.button_held(buttons, old_buttons, nowtime):
            board.move_right() 
        if up_button.button_held(buttons, old_buttons, nowtime):
            board.move_up()
        elif down_button.button_held(buttons, old_buttons, nowtime):
            board.move_down()
        if select_button.button_clicked(buttons, old_buttons, nowtime)[0]:
            game.record_dart(board.get_selected())
            game.update()
        if back_button.button_clicked(buttons, old_buttons, nowtime)[0]:
            game.undo_dart()
            game.update()

        board.update()
    root.update() 
    old_buttons = buttons
