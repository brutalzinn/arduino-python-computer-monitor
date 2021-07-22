from sys import platform
from time import sleep
import serial
import serial.tools.list_ports
from serial.serialwin32 import Serial
import json
import wmi
import threading
from hotkey import activate_hotkeys
from plataform import windows, linux
ports = serial.tools.list_ports.comports()
handShakePort = None
prevMode = 0
mode = 0
memoryActivate = False
maxMem = 0
memKey = ''
gpuKey = ''
gpuActivate = False
systemType = False
Li = 16
Lii = 0
connected = False
if platform == "linux" or platform == "linux2":
    systemType = linux()
elif platform == "win32":
    systemType = windows()
with open("config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()
maxMem = jsonObject['maxMem']
memKey = jsonObject['memKey']
gpuKey = jsonObject['gpuKey']
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
                    handShakePort = port.device
                    connected = True
                    break
            except IOError as err:
                print(err)
                ser.close()
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
myKeys = {memKey:setModeMemory,gpuKey:setModeGPU}
activate_hotkeys(myKeys)
while handShakePort != None:
    if not ser.isOpen():
        ser = serial.Serial(handShakePort, 9600)
    prepareWriter = systemType.execute()
    message = f'{prepareWriter}'
    ser.write((message).encode('ascii'))
    sleep(1)

