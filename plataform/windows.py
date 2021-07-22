import socket
from time import sleep
import json
import select

class Windows:
    def __init__(self, maxmem):
        self.maxmem = maxmem
        self.Li = 16
        self.Lii = 0
        self.HOST = '127.0.0.1'
        self.PORT = 60000       
        self.lenght = 1024 * 1024
        self.queue = []
        self.connected = False
        
        
    def handleMessage(self,message):
        response = {}
        for item in message['entries']:
            if 'GPU temperature' in item['name']:
                response['gpuTemp'] = item['data']
            elif 'GPU usage' in item['name']:
                response['gpuUsage'] = item['data']
            elif 'Fan speed' in item['name']:
                response['gpuFan'] = item['data']
            elif 'CPU temperature' in item['name']:
                response['cpuTemp'] = item['data']
            elif 'CPU usage' in item['name']:
                response['cpuUsage'] = item['data']
            elif 'RAM usage' in item['name']:
                response['ramUsage'] = item['data']
                response['ramMax'] = item['maxLimit']
                response['memUsagePercent'] = 100 * float( item['data'])/float(item['maxLimit']) 
            elif 'Framerate' in item['name']:
                response['fps'] = item['data']
        return response
    def startConnection(self):
        self.sock = socket.socket()
        host = socket.gethostname()
        self.sock.connect((host, self.PORT))
        self.sock.setblocking(0)

    def handleQueue(self):
        lastMessage = self.queue[len(self.queue) - 1]
        jsonToHandle = json.loads(lastMessage)
        self.queue.pop(len(self.queue) - 1)
        return self.handleMessage(jsonToHandle['afterburner'])
    def execute(self,mode):
        machineInfo = False
        ready = select.select([self.sock], [], [], 1)
        if ready[0]:
            data = self.sock.recv(self.lenght).decode('utf-8')
            if data:
                self.queue.append(data)
                machineInfo = self.handleQueue()
                cpuTemp = machineInfo["cpuTemp"]
                cpuPercent = machineInfo["cpuUsage"]
                maxMemStatus = '1'
                memPercent = machineInfo["memUsagePercent"]
                if memPercent > self.maxmem:
                    maxMemStatus = '1'
                else:
                    maxMemStatus = '0'
                memTotal = machineInfo["ramMax"]
                memUsed = machineInfo["ramUsage"]
                gpu_util = machineInfo["gpuUsage"]
                gpu_temp =  machineInfo["gpuTemp"]
                memInfo = f'MEM: {memPercent}% {round(memUsed,1)}GB de {round(memTotal,1)}GB'
                gpuInfo = f'GPU: {gpu_util}% {gpu_temp}C'
                procInfo = f'CPU: {cpuPercent}% {cpuTemp}C'
                def scrollText(text):
                    result = None
                    StrProcess = "                " + text + "                "
                    result = StrProcess[self.Lii: self.Li]
                    self.Li = self.Li + 1
                    self.Lii = self.Lii + 1
                    if self.Li > len(StrProcess):
                        self.Li = 16
                        self.Lii = 0
                    return result
                writerResult = {"rowone":f"{memInfo}","rowtwo":f"{procInfo}"}
                if mode == -1:
                    writerResult = {"rowone":f"{memInfo}","rowtwo":f"{procInfo}"}
                if mode == 1:
                    writerResult = {"rowone":f"{scrollText(memInfo)}","rowtwo":f"{procInfo}"}
                if mode == 3:
                    writerResult = {"rowone":f"{gpuInfo}","rowtwo":f"{procInfo}"}
                writerResult['maxmem'] = maxMemStatus
            #  print('teste')
            return writerResult