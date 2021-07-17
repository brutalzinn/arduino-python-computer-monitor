from pynput import keyboard
import threading
from time import sleep

def setModeMemory():
    print('set memory')
def setModeGPU():
    print('set gpu')
    

def activate_hotkeys(args):
    # for item in kwargs:
    #     print(item)
    listener = keyboard.GlobalHotKeys(args)
    listener.start()

myKeys = {'<ctrl>+<alt>+1':setModeMemory,'<ctrl>+<alt>+3':setModeGPU}

activate_hotkeys(myKeys)

while True:
    print('apenas uma passada do while')
    sleep(1)