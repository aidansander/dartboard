
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