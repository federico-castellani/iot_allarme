from microbit import *
import radio

#Initialize UART for serial communication
uart.init(baudrate=115200)

radio.on()
radio.config(group=33)

alarm = False
display.show(Image.NO)

while True:   
    # uart is used to read the input on the serial
    if uart.any():
        incoming = uart.read().decode('utf-8')
        if incoming == "A":
            radio.send("A")

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