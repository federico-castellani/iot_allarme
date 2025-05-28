from microbit import *
import radio

radio.on()
radio.config(group=33)

alarm = False
display.show(Image.NO)

while True:    
    message = radio.receive()
    if message:
        if message == "Alarm ON":
            alarm = True
            display.show(Image.YES)
            print("on")
        elif message == "Alarm OFF":
            alarm = False
            print("off")
            display.show(Image.NO)
        elif message == "Movement":
            print("m")
        elif message == "Alarm SILENCED":
            print("s")