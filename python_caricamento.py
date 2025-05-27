from microbit import *
import radio

radio.on()
radio.config(group=33)

alarm = False
display.show(Image.NO)

while True:    
    message = radio.receive()
    if message:
        print(message)
        if message == "Alarm ON":
            alarm = True
            display.show(Image.YES)
        elif message == "Alarm OFF":
            alarm = False
            display.show(Image.NO)