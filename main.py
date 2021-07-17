from os import error
from time import sleep
import serial
import psutil
from serial.serialwin32 import Serial
import serial.tools.list_ports
import GPUtil
import json
from hotkey import activate_gpu, activate_mem
ports = serial.tools.list_ports.comports()
handShakePort = None
prevMode = 0
mode = 0
memoryActivate = False
maxMem = 0
memKey = ''
gpuKey = ''
gpuActivate = False

Li = 16
Lii = 0
connected = False

with open("config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

maxMem = jsonObject['maxMem']
memKey = jsonObject['memKey']
gpuKey = jsonObject['gpuKey']
print('maxmem',maxMem)
ports = serial.tools.list_ports.comports(include_links=False)
ser = serial.Serial()
while not connected:
    for port in ports:
            try:
                if not ser.isOpen():
                    ser = serial.Serial(
                        port=port.device,
                        baudrate=9600,
                        timeout=1
                    )
                ser.write(b'{"status":"1"}')
                reading = ser.read_until(b'1')
                print(reading)
                if reading == b"1":
                    print('respondeu.. porta atribuida pelo handshake.')
                    handShakePort = port
                    ser.close()
                    connected = True
                    break
            except Exception as err:
                print(err)
                pass
            

def setModeMemory():
    global mode, prevMode, memoryActivate
    if not memoryActivate:
        prevMode = mode
        mode = 1
        memoryActivate = True
    else:
        mode = -1
        memoryActivate = False
def setModeGPU():
    global mode, prevMode, gpuActivate
    if not gpuActivate:
        prevMode = mode
        mode = 3
        gpuActivate = True
    else:
        mode = -3
        gpuActivate = False

activate_mem(setModeMemory,memKey)
activate_gpu(setModeGPU,gpuKey)
while handShakePort != None:
    maxMemStatus = '1'
    mem = psutil.virtual_memory()
    memPercent = mem.percent
    if memPercent > maxMem:
        maxMemStatus = '1'
    else:
        maxMemStatus = '0'
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
    memInfo = f'MEM: {memPercent}% {round(memUsed,1)}GB de {round(memTotal,1)}GB'
    gpuInfo = f'GPU: {gpu_util}% {gpu_temp} C    '
    procInfo = f'CPU: {cpuPercent}% {cpuTemp} C GPU: {gpu_util}% {gpu_temp} C'
    def modeWriter():
        global mode
        def scrollText(text):
            global Li, Lii
            result = None
            StrProcess = "                " + text + "                "
            result = StrProcess[Lii: Li]
            Li = Li + 1
            Lii = Lii + 1
            if Li > len(StrProcess):
                Li = 16
                Lii = 0
            return result
        writerResult = {"rowone":f"{memInfo}","rowtwo":f"{procInfo}"}
        if mode == -1:
            writerResult = {"rowone":f"{memInfo}","rowtwo":f"{procInfo}"}
        if mode == 1:
            writerResult = {"rowone":f"{scrollText(memInfo)}","rowtwo":f"{procInfo}"}
        if mode == 3:
            writerResult = {"rowone":f"{gpuInfo}","rowtwo":f"{procInfo}"}
        return writerResult
    #print('startig at port',handShakePort)
    ser = serial.Serial(handShakePort, 9600)
    prepareWriter = modeWriter()
    prepareWriter['maxmem'] = maxMemStatus
    message = f'{prepareWriter}\n'
    ser.write((message).encode('ascii'))
    sleep(1)

