from time import sleep
import serial
import psutil
mem = psutil.virtual_memory()
memPercent = mem.percent
memTotal = mem.total /1024/1024/1024
memUsed = mem.active /1024/1024/1024
cpuPercent = psutil.cpu_percent()

memInfo = f'{memPercent}% {round(memUsed,1)} GB de {round(memTotal,1)} GB'

ser = serial.Serial('/dev/ttyUSB0', 9600) # Establish the connection on a specific port
while True:
    ser.write(('{"mem":"'+memInfo+'"}\n').encode('ascii')) # Convert the decimal number to ASCII then send it to the Arduino
    sleep(1)
ser.close()