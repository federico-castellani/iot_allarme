import gc
from IRM import *
from microbit import *
import radio
from mb_i2c_lcd1602 import *

# LCD
l = LCD1620() #scl=19 sda=20

#garbage collector for IR receiver
gc.collect()

# Initialize radio
radio.on()
radio.config(group=33)

sens_movement= pin0 #5v Movement sensor
buzzer = pin1 #3v Buzzer
led = pin2 #5v 3w Led
sens_ir = pin12 #3v IR receiver

# traffic lights
green_light = pin15
yellow_light = pin14
red_light = pin13

# IR receiver setup
sens_ir.set_pull(sens_ir.PULL_UP)
d = IRM()

# Remote keys mapping
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

# Alarm initial state
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

# Function used to switch the alarm state
def turn_alarm():

    global alarm
    alarm = not alarm #change the state of the alarm

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

# function used to silence the alarm
def silence_alarm():
    global movement, light
    
    if movement:
        radio.send("Alarm SILENCED")
        print("Alarm has been silenced")
        yellow_light.write_digital(0)
        movement = False
        light = False
        led.write_digital(0)
        buzzer.write_digital(0)

# Main loop
while True:
    # check if the radio received a message
    # and if the message is "A", turn the alarm on or off
    message = radio.receive()
    if message:

        if message == "A":
            turn_alarm()

        elif message == "S":
            silence_alarm()

    # check if the alarm is on
    if movement:
        led.write_digital(light)
        light = not light

    # get value from the IR receiver
    key = d.get(sens_ir)
    if key!=-1:
        key = remote_keys[key] #replace the key code with the button that was pressed

        # Silence the alarm only after the button OK is pressed
        if key == "OK":
            silence_alarm()

        # Clear the digits entered when "#" is pressed
        if key == "#":
            code_input.clear()
            l.puts("    ", 0, 0)
        
        # Check if the key pressed is a number
        if type(key) == type(0):

            # ord function converts the ascii value of the key to a character
            l.char(ord(str(key)), len(code_input), 0) # write key on lcd

            # append the key to the code input
            code_input.append(key)

            # check if the code given is correct, after 4 digits are entered
            if len(code_input) == 4:

                # Right code is 8086
                if alarm_code == code_input:
                    turn_alarm()
                    code_input.clear()
                    l.puts("    ", 0, 0)

                # Wrong code, clear the input
                else:
                    code_input.clear()
                    l.puts("    ", 0, 0)

        print(code_input)       

    # movement sensor check
    if sens_movement.read_digital() == 1 and not movement and alarm:
        print("Movement")
        radio.send("Movement")
        yellow_light.write_digital(1)
        movement = True
        light = True
        buzzer.write_digital(1)