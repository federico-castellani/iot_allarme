import gc
from IRM import *
from microbit import *
import radio

gc.collect()
radio.on()
radio.config(group=33)

sens_movement= pin0 #5v
sens_ir = pin12 #3v

sens_ir.set_pull(sens_ir.PULL_UP)
d = IRM()

remote_keys = {
    22: 1, 25: 2, 13: 3,
    12: 4, 24: 5, 94: 6,
    8: 7,  28: 8, 90: 9,
    66: "*", 82: 0, 74: "#",
    70: "UP",
    67: "RIGHT",
    68: "LEFT",
    21: "DOWN",
    64: "OK"
}

alarm = True
alarm_code = [8, 0, 8, 6]
code_input = []

movement = False

while True:
    key = d.get(sens_ir)
    if key!=-1:
        key = remote_keys[key] #replace the key code with the button that was pressed
        display.show(key)

        #check if the key pressed is the right one at the correct index
        if key == alarm_code[len(code_input)]:
            code_input.append(key) #if right i add it to the correct keys pressed
            
            if alarm_code == code_input:
                alarm = not alarm #change the state of the alarm
                radio.send("Alarm")
                if alarm:
                    print("Alarm has been turned on")
                else:
                    print("Alarm has been turned off")
                code_input.clear()
                display.show(Image.YES)
        else:
            code_input.clear()
            display.show(Image.NO)

        print(code_input)

    if sens_movement.read_digital() == 0: 
        #limit to 1 the amount of outputs of the movement sensor
        movement = False

    if sens_movement.read_digital() == 1 and not movement and alarm:
        print("Movement")
        radio.send("Movement")
        movement = True