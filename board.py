import tkinter as tk
import time
import tkinter.font as tkFont
from enum import IntEnum
import math

from dart import Dart

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

        #print ("selection=", self.get_selected())

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


class Arcy(IntEnum):
    MISS = 0
    DOUBLE_ARC = 1
    SINGLE_ARC_OUTER = 2
    TRIPLE_ARC  = 3
    SINGLE_ARC_INNER = 4
    BULL  = 5
    DOUBLE_BULL  = 6