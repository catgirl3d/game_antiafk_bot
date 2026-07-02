import os
import webview
import json
import threading
from core.bot import AntiAfkBot

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

class Api:
    def __init__(self):
        self.bot = AntiAfkBot()
        self.settings = self._load_settings()
        self.settings_lock = threading.RLock()

    def _load_settings(self):
        defaults = {
            "keys": "space",
            "interval_min": 4.5,
            "interval_max": 7.0,
            "randomize_enabled": False,
            "press_duration_min": 50,
            "press_duration_max": 150,
            "micro_movements": False,
            "random_clicks": False,
            "cursor_move_pixels": 15,
            "always_on_top": False,
            "x": None,
            "y": None
        }
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    settings = json.load(f)
                    # Merge defaults with loaded settings
                    defaults.update(settings)
                    # Reset if coordinates are invalid
                    if defaults.get("x", 0) < -10000 or defaults.get("y", 0) < -10000:
                        defaults["x"] = None
                        defaults["y"] = None
                    return defaults
            except Exception:
                pass
        return defaults

    def _save_settings(self, x=None, y=None):
        try:
            with self.settings_lock:
                if x is not None and x > -10000:
                    self.settings["x"] = x
                if y is not None and y > -10000:
                    self.settings["y"] = y

                with open(CONFIG_FILE, 'w') as f:
                    json.dump(self.settings, f)
        except Exception as e:
            print(f"DEBUG: Error saving settings: {e}")

    def _save_window_position(self):
        window = webview.active_window()
        if window and window.x > -10000 and window.y > -10000:
            self._save_settings(window.x, window.y)
        else:
            self._save_settings()

    def save_settings(self, settings_dict):
        try:
            print(f"DEBUG: save_settings called with: {settings_dict}")
            with self.settings_lock:
                self.settings.update(settings_dict)
                self._save_settings()
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_settings(self):
        with self.settings_lock:
            return dict(self.settings)

    def start_bot(self, settings_dict):
        try:
            print(f"DEBUG: start_bot called with: {settings_dict}")
            with self.settings_lock:
                self.settings.update(settings_dict)
                self._save_settings()
            self.bot.start(settings_dict)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def stop_bot(self):
        try:
            print("DEBUG: stop_bot called")
            self._save_window_position()
            self.bot.stop()
            return {"status": "success"}
        except Exception as e:
            print(f"DEBUG: Error in stop_bot: {e}")
            return {"status": "error", "message": str(e)}

    def get_bot_status(self):
        try:
            return self.bot.get_status()
        except Exception as e:
            print(f"DEBUG: Error in get_bot_status: {e}")
            return {
                "running": False,
                "phase": "idle",
                "action_count": 0,
                "started_at_ms": None,
                "current_interval_seconds": None,
                "remaining_seconds": 0.0,
                "progress": 0.0,
            }

    def minimize_window(self):
        window = webview.active_window()
        if window:
            self._save_window_position()
            window.minimize()
        return True

    def close_window(self):
        window = webview.active_window()
        if window:
            self._save_window_position()
            window.destroy()
        return True

    def resize_window(self, width, height):
        window = webview.active_window()
        if window:
            window.resize(int(width), int(height))
        return True

    def set_always_on_top(self, on_top):
        try:
            print(f"DEBUG: Setting always_on_top to {on_top}")
            with self.settings_lock:
                self.settings["always_on_top"] = on_top
                self._save_settings()
            
            window = webview.active_window()
            if window:
                window.on_top = on_top
                return True
            return False
        except Exception as e:
            print(f"DEBUG: Error setting always on top: {e}")
            return False

def get_asset_path(filename):
    return os.path.join(os.path.dirname(__file__), 'assets', filename)


def create_main_window(api, html_url):
    return webview.create_window(
        'Anti-AFK Bot',
        url=html_url,
        width=500,
        height=650,
        x=api.settings.get("x"),
        y=api.settings.get("y"),
        resizable=True,
        frameless=True,
        easy_drag=False,
        js_api=api,
        on_top=api.settings.get("always_on_top", False),
        background_color='#0f0f1a'
    )

if __name__ == '__main__':
    api = Api()
    
    html_path = get_asset_path('index.html')
    html_url = f'file://{os.path.abspath(html_path)}'

    window = create_main_window(api, html_url)
    
    def on_moved(x, y):
        api._save_settings(x, y)

    window.events.moved += on_moved
    
    webview.start()
    
    # Ensure bot stops when window closes
    api.bot.stop()
