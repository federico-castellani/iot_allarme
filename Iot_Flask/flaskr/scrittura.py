import serial
import time

ser = serial.Serial('/dev/ttyACM1', 115200)

time.sleep(1)

ser.write(b'A\n')
ser.flush()