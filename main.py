from pynput import keyboard
import time
import threading

class StenographyReplacer:
    def __init__(self):
        self.steno_dict = {
            'ex': 'example'
        }
        self.last_key_time = 0
        self.buffer = ''
        self.is_replacing = False

    def on_press(self, key):
        if self.is_replacing:
            return

        current_time = time.time()
        
        try:
            char = key.char
        except AttributeError:
            char = str(key)
        
        if current_time - self.last_key_time <= 0.1:
            self.buffer += char
        else:
            self.buffer = char
        
        self.last_key_time = current_time
        
        for steno_key, value in self.steno_dict.items():
            if self.buffer.endswith(steno_key):
                self.is_replacing = True
                threading.Thread(target=self.replace_text, args=(steno_key, value)).start()
                break

    def replace_text(self, old_text, new_text):
        controller = keyboard.Controller()
        
        for _ in range(len(old_text)):
            controller.press(keyboard.Key.backspace)
            controller.release(keyboard.Key.backspace)
            time.sleep(0.01)
        
        controller.type(new_text)
        
        self.buffer = ''
        self.is_replacing = False

    def start_replacing(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    replacer = StenographyReplacer()
    replacer.start_replacing()