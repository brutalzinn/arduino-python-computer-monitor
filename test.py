import serial
from time import sleep
ser = serial.Serial('COM6', 9600, timeout=0)
while True:
    
    ser.write(b'{"status":"1"}')
    reading = ser.read(ser.inWaiting()).decode('ascii')
    print(reading)
