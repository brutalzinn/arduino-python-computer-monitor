from os import error
from time import sleep
import serial
import psutil
import serial.tools.list_ports
import GPUtil


ports = serial.tools.list_ports.comports()
handShakePort = ''
for port, desc, hwid in sorted(ports):
        # print("{}: {} [{}]".format(port, desc, hwid))
        try:
            testHandShake = serial.Serial(port, 9600)
            testHandShake.write('{"status":"1"}'.encode())
            response = testHandShake.read_until(b"1\n")
            print('connected to 2', port)

            if response == b"1":
                print('respondeu.. porta atribuida pelo handshake.')
                handShakePort = port
                testHandShake.close()
                break

        except Exception as err:
            print(err)
            pass


mem = psutil.virtual_memory()
memPercent = mem.percent
memTotal = mem.total /1024/1024/1024
memUsed = mem.active /1024/1024/1024
cpuPercent = psutil.cpu_percent()
gpu = GPUtil.getGPUs()[0]
gpu_util = int(gpu.load * 100)
gpu_temp = int(gpu.temperature)
cpuTemp = 0
cpuTemps = psutil.sensors_temperatures()['coretemp']
for item in cpuTemps:
    if 'Package' in item.label:
        cpuTemp = item.current

memInfo = f'MEM: {memPercent}% {round(memUsed,1)} GB de {round(memTotal,1)} GB'
procInfo = f'CPU: {cpuPercent}% {cpuTemp} C GPU: {gpu_util}% {gpu_temp} C'
ser = serial.Serial(handShakePort, 9600)
while True:
    ser.write(('{"rowone":"'+memInfo+'","rowtwo":"'+procInfo+'"}').encode())
    sleep(1)
