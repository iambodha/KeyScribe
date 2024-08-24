from pynput import keyboard
import time
import threading

class KeyLogger:
    def __init__(self):
        self.last_time = None
        self.intervals = []
        self.running = True

    def on_press(self, key):
        current_time = time.time()

        if self.last_time is not None:
            time_interval = current_time - self.last_time
            self.intervals.append(time_interval)

        self.last_time = current_time

    def on_release(self, key):
        if key == keyboard.Key.esc:
            print("Exiting...")
            self.running = False
            return False

    def calculate_average_interval(self, period):
        while self.running:
            time.sleep(period)
            if self.intervals:
                average_interval = sum(self.intervals) / len(self.intervals)
                print(f'Average interval over last {period} seconds: {average_interval:.4f} seconds')
                self.intervals.clear()
            else:
                print(f'No key presses recorded in the last {period} seconds.')

    def start_logging(self, period=5):
        thread = threading.Thread(target=self.calculate_average_interval, args=(period,))
        thread.start()

        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

        self.running = False
        thread.join()

if __name__ == "__main__":
    key_logger = KeyLogger()
    key_logger.start_logging(period=5)
