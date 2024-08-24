from pynput import keyboard
import time

steno_dict = {
    'ex': 'example'
}

last_key_time = 0
buffer = ''

def on_press(key):
    global last_key_time, buffer
    
    current_time = time.time()
    
    try:
        char = key.char
    except AttributeError:
        char = key.name
    
    if current_time - last_key_time <= 0.1:
        buffer += char
    else:
        buffer = char
    
    last_key_time = current_time
    
    for key, value in steno_dict.items():
        if buffer.endswith(key):
            for _ in range(len(key)):
                keyboard.Controller().press(keyboard.Key.backspace)
                keyboard.Controller().release(keyboard.Key.backspace)
            
            keyboard.Controller().type(value)
            
            buffer = ''
            break

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()