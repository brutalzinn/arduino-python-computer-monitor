import socket
from time import sleep
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 60000        # The port used by the server
lenght = 1024 * 1024
queue = []
def handleMessage(message):
    response = {}
    response = message['afterburner']
    gpuTemp = 0
    for item in response['entries']:
        if 'GPU temperature' in item['name']:
            gpuTemp = item['data']
    return response
def handleQueue():
    lastMessage = queue[len(queue) - 1]
    jsonToHandle = json.loads(lastMessage)
    handleMessage(jsonToHandle)
    queue.clear()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(lenght).decode('utf-8')
    queue.append(data)
    handleQueue()
    s.close()