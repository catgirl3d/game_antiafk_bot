import importlib
import json
import os
import sys
import tempfile
import types
import unittest
from unittest.mock import patch


pyautogui_stub = types.SimpleNamespace(
    moveRel=lambda *args, **kwargs: None,
    click=lambda *args, **kwargs: None,
    keyDown=lambda *args, **kwargs: None,
    keyUp=lambda *args, **kwargs: None,
)
webview_stub = types.SimpleNamespace(
    create_window=lambda *args, **kwargs: None,
    active_window=lambda: None,
)

sys.modules.setdefault("pyautogui", pyautogui_stub)
sys.modules.setdefault("webview", webview_stub)

main = importlib.import_module("main")


class MainWindowTests(unittest.TestCase):
    def test_create_main_window_disables_easy_drag(self):
        api = types.SimpleNamespace(settings={"x": 10, "y": 20, "always_on_top": True})

        with patch.object(main.webview, "create_window", return_value="window") as create_window:
            result = main.create_main_window(api, "file:///tmp/index.html")

        self.assertEqual(result, "window")
        self.assertEqual(create_window.call_args.args, ("Anti-AFK Bot",))
        self.assertEqual(create_window.call_args.kwargs["url"], "file:///tmp/index.html")
        self.assertTrue(create_window.call_args.kwargs["frameless"])
        self.assertFalse(create_window.call_args.kwargs["easy_drag"])
        self.assertEqual(create_window.call_args.kwargs["js_api"], api)

    def test_save_settings_does_not_query_active_window(self):
        api = main.Api()

        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = os.path.join(tmp_dir, "config.json")

            with patch.object(main, "CONFIG_FILE", config_path), \
                 patch.object(main.webview, "active_window", side_effect=AssertionError("active_window should not be used")):
                response = api.save_settings({"always_on_top": True})

            self.assertEqual(response, {"status": "success"})

            with open(config_path, "r") as saved_file:
                saved_settings = json.load(saved_file)

            self.assertTrue(saved_settings["always_on_top"])

    def test_set_always_on_top_updates_window_and_settings(self):
        api = main.Api()
        window = types.SimpleNamespace(on_top=False, x=10, y=20)

        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = os.path.join(tmp_dir, "config.json")

            with patch.object(main, "CONFIG_FILE", config_path), \
                 patch.object(main.webview, "active_window", return_value=window):
                result = api.set_always_on_top(True)

            self.assertTrue(result)
            self.assertTrue(window.on_top)
            self.assertTrue(api.settings["always_on_top"])

            with open(config_path, "r") as saved_file:
                saved_settings = json.load(saved_file)

            self.assertTrue(saved_settings["always_on_top"])

    def test_save_window_position_uses_active_window_coordinates(self):
        api = main.Api()
        window = types.SimpleNamespace(x=123, y=456)

        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = os.path.join(tmp_dir, "config.json")

            with patch.object(main, "CONFIG_FILE", config_path), \
                 patch.object(main.webview, "active_window", return_value=window):
                api._save_window_position()

            with open(config_path, "r") as saved_file:
                saved_settings = json.load(saved_file)

            self.assertEqual(saved_settings["x"], 123)
            self.assertEqual(saved_settings["y"], 456)


if __name__ == "__main__":
    unittest.main()
