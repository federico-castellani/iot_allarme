from microbit import *
import radio

radio.on()
radio.config(group=33)

alarm = True
display.show(Image.YES)

while True:
    message = radio.receive()
    if message:
        if message == "Alarm":
            alarm = not alarm
            if alarm:
                display.show(Image.YES)
            else:
                display.show(Image.NO)
        print(message)
        