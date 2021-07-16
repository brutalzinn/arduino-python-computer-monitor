from pynput import keyboard

def activate_mem(on_fix_memory,key):

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse(key),
        on_fix_memory)
    listener = keyboard.Listener(
            on_press=hotkey.press,
            on_release=hotkey.release)
    listener.start()
def activate_gpu(on_fix_gpu, key):

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse(key),
        on_fix_gpu)
    listener = keyboard.Listener(
            on_press=hotkey.press,
            on_release=hotkey.release)
    listener.start()
