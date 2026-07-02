import threading
import time
import random
import pyautogui

# Constants
RANDOM_CLICK_PROBABILITY = 0.05  # 5% chance for random clicks
DEFAULT_CURSOR_MOVE_PIXELS = 15

class AntiAfkBot:
    def __init__(self):
        self.running = False
        self.thread = None
        self.state_lock = threading.RLock()
        
        # Settings
        self.keys = []
        self.interval_min = 5.0
        self.interval_max = 5.0
        self.randomize_enabled = False
        self.press_duration_min = 0.05
        self.press_duration_max = 0.15
        self.micro_movements = False
        self.random_clicks = False
        self.cursor_move_pixels = DEFAULT_CURSOR_MOVE_PIXELS
        self.started_at = None
        self.next_action_at = None
        self.interval_started_at = None
        self.current_interval = 0.0
        self.action_count = 0
        self.phase = 'idle'

    def start(self, settings):
        """Start bot with settings dict"""
        if self.running:
            return

        self._reset_runtime_state()
        
        # Parse settings
        keys_str = settings.get('keys', 'space')
        self.keys = [k.strip() for k in keys_str.split(',') if k.strip()]
        
        self.interval_min = float(settings.get('interval_min', 5.0))
        self.interval_max = float(settings.get('interval_max', 5.0))
        self.randomize_enabled = settings.get('randomize_enabled', False)
        
        # Convert ms to seconds
        self.press_duration_min = float(settings.get('press_duration_min', 50)) / 1000.0
        self.press_duration_max = float(settings.get('press_duration_max', 150)) / 1000.0
        
        self.micro_movements = settings.get('micro_movements', False)
        self.random_clicks = settings.get('random_clicks', False)
        try:
            self.cursor_move_pixels = max(1, int(settings.get('cursor_move_pixels', DEFAULT_CURSOR_MOVE_PIXELS)))
        except (TypeError, ValueError):
            self.cursor_move_pixels = DEFAULT_CURSOR_MOVE_PIXELS

        with self.state_lock:
            self.started_at = time.time()
            self.phase = 'acting'

        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None
        self._reset_runtime_state()

    def _get_random_interval(self):
        """Get random interval between min and max"""
        if self.randomize_enabled:
            return random.uniform(self.interval_min, self.interval_max)
        return self.interval_min

    def _get_random_key(self):
        """Select random key from list"""
        if not self.keys:
            return 'space'
        return random.choice(self.keys)

    def _get_random_duration(self):
        """Get random press duration"""
        return random.uniform(self.press_duration_min, self.press_duration_max)

    def _do_micro_movement(self):
        """Random micro cursor movement"""
        if not self.micro_movements:
            return
        
        try:
            dx = random.randint(-self.cursor_move_pixels, self.cursor_move_pixels)
            dy = random.randint(-self.cursor_move_pixels, self.cursor_move_pixels)
            pyautogui.moveRel(dx, dy, duration=0.1)
            print(f"DEBUG: Micro-movement ({dx}, {dy})")
        except Exception as e:
            print(f"DEBUG: Micro-movement error: {e}")

    def _do_random_click(self):
        """Random mouse click with 5% probability"""
        if not self.random_clicks:
            return
        
        if random.random() < RANDOM_CLICK_PROBABILITY:
            try:
                button = random.choice(['left', 'right'])
                pyautogui.click(button=button)
                print(f"DEBUG: Random {button} click")
            except Exception as e:
                print(f"DEBUG: Random click error: {e}")

    @staticmethod
    def _to_epoch_ms(timestamp):
        if timestamp is None:
            return None
        return int(timestamp * 1000)

    def _reset_runtime_state(self):
        with self.state_lock:
            self.started_at = None
            self.next_action_at = None
            self.interval_started_at = None
            self.current_interval = 0.0
            self.action_count = 0
            self.phase = 'idle'

    def _set_phase(self, phase):
        with self.state_lock:
            self.phase = phase
            if phase != 'waiting':
                self.next_action_at = None
                self.interval_started_at = None
                self.current_interval = 0.0

    def _record_action(self):
        with self.state_lock:
            self.action_count += 1

    def _schedule_next_action(self, interval, timestamp=None):
        if timestamp is None:
            timestamp = time.time()

        with self.state_lock:
            self.phase = 'waiting'
            self.interval_started_at = timestamp
            self.current_interval = interval
            self.next_action_at = timestamp + interval

    def get_status(self):
        now = time.time()

        with self.state_lock:
            running = self.running
            phase = self.phase
            started_at = self.started_at
            next_action_at = self.next_action_at
            interval_started_at = self.interval_started_at
            current_interval = self.current_interval
            action_count = self.action_count

        remaining_seconds = 0.0
        progress = 0.0 if not running else 1.0

        if (
            running
            and phase == 'waiting'
            and current_interval > 0
            and interval_started_at is not None
            and next_action_at is not None
        ):
            remaining_seconds = max(0.0, next_action_at - now)
            elapsed_seconds = min(current_interval, max(0.0, now - interval_started_at))
            progress = min(1.0, elapsed_seconds / current_interval)

        return {
            'running': running,
            'phase': phase,
            'action_count': action_count,
            'started_at_ms': self._to_epoch_ms(started_at),
            'current_interval_seconds': current_interval if current_interval > 0 else None,
            'remaining_seconds': remaining_seconds,
            'progress': progress,
        }

    def _run_loop(self):
        print(f"DEBUG: Thread started with keys: {self.keys}")
        try:
            while self.running:
                self._set_phase('acting')

                # Select random key
                key = self._get_random_key()
                duration = self._get_random_duration()
                
                # Press key with random duration
                print(f"DEBUG: Pressing '{key}' for {duration:.3f}s")
                pyautogui.keyDown(key)
                time.sleep(duration)
                pyautogui.keyUp(key)
                
                # Random mouse actions
                self._do_micro_movement()
                self._do_random_click()

                action_completed_at = time.time()
                self._record_action()

                if not self.running:
                    break
                
                # Wait for next action
                interval = self._get_random_interval()
                self._schedule_next_action(interval, action_completed_at)
                print(f"DEBUG: Next action in {interval:.2f}s")
                
                # Sleep in small chunks to allow faster stopping
                elapsed = 0.0
                while elapsed < interval and self.running:
                    sleep_time = min(0.1, interval - elapsed)
                    time.sleep(sleep_time)
                    elapsed += sleep_time
                    
        except Exception as e:
            print(f"DEBUG: Exception in thread: {e}")
            self.running = False
        self._reset_runtime_state()
        print("DEBUG: Thread finished")
