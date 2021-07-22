import socket
from time import sleep
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 60000        # The port used by the server
lenght = 1024 * 1024
queue = []
def handleMessage(message):
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
    #return response
def handleQueue():
    lastMessage = queue[len(queue) - 1]
    jsonToHandle = json.loads(lastMessage)
    handleMessage(jsonToHandle['afterburner'])
    queue.pop(len(queue) - 1)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(lenght).decode('utf-8')
        if data:
            queue.append(data)
            handleQueue()
            sleep(1)
   # s.close()