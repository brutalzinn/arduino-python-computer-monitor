from pynput import keyboard
def activate_hotkeys(args):
    listener = keyboard.GlobalHotKeys(args)
    listener.start()