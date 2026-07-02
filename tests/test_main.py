import importlib
import sys
import types
import unittest
from unittest.mock import patch


pyautogui_stub = types.SimpleNamespace(
    moveRel=lambda *args, **kwargs: None,
    click=lambda *args, **kwargs: None,
    keyDown=lambda *args, **kwargs: None,
    keyUp=lambda *args, **kwargs: None,
)
webview_stub = types.SimpleNamespace(create_window=lambda *args, **kwargs: None)

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


if __name__ == "__main__":
    unittest.main()
