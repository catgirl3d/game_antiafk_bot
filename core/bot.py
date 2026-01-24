import threading
import time
import pyautogui

class AntiAfkBot:
    def __init__(self):
        self.running = False
        self.thread = None
        self.key = None
        self.interval = None

    def start(self, key, interval):
        if self.running:
            return
        self.key = key
        self.interval = float(interval)
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None

    def _run_loop(self):
        print(f"DEBUG: Thread started for key '{self.key}'")
        try:
            while self.running:
                print(f"DEBUG: Pressing '{self.key}'")
                pyautogui.press(self.key)
                # Sleep in small chunks to allow faster stopping
                for _ in range(int(self.interval * 10)):
                    if not self.running:
                        break
                    time.sleep(0.1)
        except Exception as e:
            print(f"DEBUG: Exception in thread: {e}")
            self.running = False
        print("DEBUG: Thread finished")
