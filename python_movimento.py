import gc
from IRM import *
from microbit import *
import radio
from mb_i2c_lcd1602 import *

uart.init(baudrate=115200)

l = LCD1620() #scl=19 sda=20

gc.collect()
radio.on()
radio.config(group=33)

sens_movement= pin0 #5v
buzzer = pin1 #3v
led = pin2 #5v
sens_ir = pin12 #3v

green_light = pin15
yellow_light = pin14
red_light = pin13

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

alarm = False
alarm_code = [8, 0, 8, 6]
code_input = []

movement = False

green_light.write_digital(0)
yellow_light.write_digital(0)
red_light.write_digital(1)

led.write_digital(0)

l.puts("Alarm OFF", 0, 1)

light = False

def turn_alarm():
    if alarm:
        radio.send("Alarm ON")
        print("Alarm has been turned on")
        green_light.write_digital(1)
        red_light.write_digital(0)
        l.puts("Alarm ON ", 0, 1)
    else:
        radio.send("Alarm OFF")
        print("Alarm has been turned off")
        green_light.write_digital(0)
        red_light.write_digital(1)
        l.puts("Alarm OFF", 0, 1)

while True:
    #uart is used to read the input on the serial
    if uart.any():
        incoming = uart.read().decode('utf-8')
        display.show(incoming)
        print(incoming)
        if incoming == "A":
            turn_alarm()
        else:
            display.show(Image.NO)
    
    if movement:
        led.write_digital(light)
        light = not light
    
    key = d.get(sens_ir)
    if key!=-1:
        key = remote_keys[key] #replace the key code with the button that was pressed

        #silence the alarm only after the button OK is pressed
        if key == "OK" and movement:
            radio.send("Alarm SILENCED")
            print("Alarm has been silenced")
            yellow_light.write_digital(0)
            movement = False
            light = False
            led.write_digital(0)
            buzzer.write_digital(0)

        #clear the digits entered
        if key == "#":
            code_input.clear()
            l.puts("    ", 0, 0)
        
        #check if the key pressed is a number
        if type(key) == type(0):
            #ord function converts the ascii value of the key to a character
            l.char(ord(str(key)), len(code_input), 0) #write key on lcd
            
            code_input.append(key) #if right i add it to the correct keys pressed

            if len(code_input) == 4:
                if alarm_code == code_input:
                    alarm = not alarm #change the state of the alarm
                    turn_alarm()
                    code_input.clear()
                    l.puts("    ", 0, 0)
                else:
                    code_input.clear()
                    l.puts("    ", 0, 0)

        print(code_input)       

    if sens_movement.read_digital() == 1 and not movement and alarm:
        print("Movement")
        radio.send("Movement")
        yellow_light.write_digital(1)
        movement = True
        light = True
        buzzer.write_digital(1)