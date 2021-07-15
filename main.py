from os import error
from time import sleep
import serial
import psutil
import serial.tools.list_ports
import GPUtil
from hotkey import activate_mem
ports = serial.tools.list_ports.comports()
handShakePort = None
mode = 0

Li = 16
Lii = 0
connected = False



while not connected:
    for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
            try:
                print('connecting...',port)
                testHandShake = serial.Serial(port, 9600, timeout=1.0)
                print('writing to arduino...')
                testHandShake.write('{"status":"1"}\n'.encode('ascii'))
                # print('trying to handshake..')
                # print(testHandShake.readline())

                response = testHandShake.read_until(b'1\n')
                print(response)
                if response == b"1\r\n":
                    print('respondeu.. porta atribuida pelo handshake.', port)
                    handShakePort = port
                    testHandShake.close()
                    connected = True
                    break
            except:
                pass

def setModeValue():
    global mode
    mode = 1

activate_mem(setModeValue)

while handShakePort != None:
    def modeWriter():
        global mode
        print('mode writer called')
        print('mode',mode)
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
        writerResult = '{"rowone":"'+memInfo+'","rowtwo":"'+procInfo+'"}\n'
        if mode == 1:
            writerResult = '{"rowone":"'+scrollText(memInfo)+'","rowtwo":"'+procInfo+'"}\n'
        return writerResult
    #print('startig at port',handShakePort)
    ser = serial.Serial(handShakePort, 9600)

    ser.write((modeWriter()).encode('ascii'))
    sleep(1)

