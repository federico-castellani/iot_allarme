from microbit import *
import radio

#Initialize UART for serial communication
uart.init(baudrate=115200)

radio.on()
radio.config(group=33)

alarm = False
display.show(Image.NO)

# needed to limit the inputs of touched to the other microbit
logo_touched = False

while True:   
    # silence the alarm if logo is touched and has not been touched before
    if pin_logo.is_touched() and not logo_touched:
        logo_touched = True
        print("touched")
        radio.send("S")
    # reset logo_touched after the inputs stop
    elif not pin_logo.is_touched() and logo_touched:
        logo_touched = False
        
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