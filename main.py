import os
import webview
import json
from core.bot import AntiAfkBot

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

class Api:
    def __init__(self):
        self.bot = AntiAfkBot()
        self.settings = self._load_settings()

    def _load_settings(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    settings = json.load(f)
                    # Reset if coordinates are invalid (minimized state on Windows)
                    if settings.get("x", 0) < -10000 or settings.get("y", 0) < -10000:
                        settings["x"] = None
                        settings["y"] = None
                    return settings
            except:
                pass
        return {"key": "space", "interval": 5.0, "always_on_top": False, "x": None, "y": None}

    def _save_settings(self, x=None, y=None):
        try:
            # Validate and save provided coordinates
            if x is not None and x > -10000: self.settings["x"] = x
            if y is not None and y > -10000: self.settings["y"] = y
            
            # If coordinates weren't passed, try to get them from active window
            if x is None or y is None:
                window = webview.active_window()
                if window and window.x > -10000 and window.y > -10000:
                    self.settings["x"] = window.x
                    self.settings["y"] = window.y
            
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"DEBUG: Error saving settings: {e}")

    def get_settings(self):
        return self.settings

    def start_bot(self, key, interval):
        try:
            print(f"DEBUG: start_bot called with Key='{key}', Interval='{interval}'")
            self.settings["key"] = key
            self.settings["interval"] = interval
            self._save_settings()
            
            self.bot.start(key, interval)
            return {"status": "success"}
        except Exception as e:
            print(f"DEBUG: Error in start_bot: {e}")
            return {"status": "error", "message": str(e)}

    def stop_bot(self):
        try:
            print("DEBUG: stop_bot called")
            self._save_settings() # Save position when stopping too
            self.bot.stop()
            return {"status": "success"}
        except Exception as e:
            print(f"DEBUG: Error in stop_bot: {e}")
            return {"status": "error", "message": str(e)}

    def minimize_window(self):
        window = webview.active_window()
        if window:
            self._save_settings()
            window.minimize()
        return True

    def close_window(self):
        window = webview.active_window()
        if window:
            self._save_settings()
            window.destroy()
        return True

    def set_always_on_top(self, on_top):
        try:
            print(f"DEBUG: Setting always_on_top to {on_top}")
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

if __name__ == '__main__':
    api = Api()
    
    html_path = get_asset_path('index.html')
    html_url = f'file://{os.path.abspath(html_path)}'

    window = webview.create_window(
        'Anti-AFK Bot', 
        url=html_url,
        width=380,
        height=520, 
        x=api.settings.get("x"),
        y=api.settings.get("y"),
        resizable=False,
        frameless=True,
        js_api=api,
        on_top=api.settings.get("always_on_top", False),
        background_color='#0f0f1a'
    )
    
    def on_moved(x, y):
        api._save_settings(x, y)

    window.events.moved += on_moved
    
    webview.start()
    
    # Ensure bot stops when window closes
    api.bot.stop()
