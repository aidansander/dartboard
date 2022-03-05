import cwiid as cw

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