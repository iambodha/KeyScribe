from pynput import keyboard
import time

class KeyLogger:
    def __init__(self):
        self.last_time = None

    def on_press(self, key):
        current_time = time.time()

        if self.last_time is not None:
            time_interval = current_time - self.last_time
            print(f'Time since last press: {time_interval:.4f} seconds')
        else:
            print("First key press!")

        try:
            print(f'Key pressed: {key.char}')
        except AttributeError:
            print(f'Special key pressed: {key}')

        self.last_time = current_time

    def on_release(self, key):
        if key == keyboard.Key.esc:
            print("Exiting...")
            return False

    def start_logging(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    key_logger = KeyLogger()
    key_logger.start_logging()
