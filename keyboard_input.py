import keyboard
from button import Button
import time

class KeyboardInput:

    def __init__(self, hold_delay = .1, button_delay = 0.4):
        self.button_bits = 0
        self.last_button_bits = 0
        self.buttons = {
            "left":Button(1, button_delay, hold_delay),
            "right":Button(2, button_delay, hold_delay),
            "up":Button(4, button_delay, hold_delay),
            "down":Button(8, button_delay, hold_delay),
            "enter":Button(16, button_delay, hold_delay),
            "backspace":Button(32, button_delay, hold_delay)
        }
        

    def update_button_bits(self):
        self.last_button_bits=self.button_bits
        self.button_bits = 0
        self.nowtime = time.time()

        for k, v in self.buttons.items():
            if keyboard.is_pressed(k):
                self.button_bits +=v.buttonmask

    def button_held(self, name):
        return self.buttons[name].button_held(self.button_bits, self.last_button_bits, self.nowtime)

    def button_clicked(self, name):
        return self.buttons[name].button_clicked(self.button_bits, self.last_button_bits, self.nowtime)[0]