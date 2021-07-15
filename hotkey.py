from pynput import keyboard

def activate_mem(on_fix_memory):

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<alt>+1'),
        on_fix_memory)
    listener = keyboard.Listener(
            on_press=hotkey.press,
            on_release=hotkey.release)
    listener.start()

