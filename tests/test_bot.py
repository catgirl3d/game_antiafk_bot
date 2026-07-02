import sys
import types
import unittest
from unittest.mock import call, patch


pyautogui_stub = types.SimpleNamespace(
    moveRel=lambda *args, **kwargs: None,
    click=lambda *args, **kwargs: None,
    keyDown=lambda *args, **kwargs: None,
    keyUp=lambda *args, **kwargs: None,
)
sys.modules.setdefault("pyautogui", pyautogui_stub)

from core.bot import AntiAfkBot, DEFAULT_CURSOR_MOVE_PIXELS


class AntiAfkBotTests(unittest.TestCase):
    def test_start_reads_cursor_move_pixels(self):
        bot = AntiAfkBot()

        with patch("core.bot.threading.Thread") as thread_cls:
            bot.start({"keys": "space", "cursor_move_pixels": 24})

        self.assertEqual(bot.cursor_move_pixels, 24)
        thread_cls.return_value.start.assert_called_once_with()

    def test_start_falls_back_to_default_cursor_move_pixels(self):
        bot = AntiAfkBot()

        with patch("core.bot.threading.Thread"):
            bot.start({"keys": "space", "cursor_move_pixels": "bad"})

        self.assertEqual(bot.cursor_move_pixels, DEFAULT_CURSOR_MOVE_PIXELS)

    def test_micro_movement_uses_configured_cursor_move_pixels(self):
        bot = AntiAfkBot()
        bot.micro_movements = True
        bot.cursor_move_pixels = 24

        with patch("core.bot.random.randint", side_effect=[-24, 17]) as randint:
            with patch("core.bot.pyautogui.moveRel") as move_rel:
                bot._do_micro_movement()

        self.assertEqual(randint.call_args_list, [call(-24, 24), call(-24, 24)])
        move_rel.assert_called_once_with(-24, 17, duration=0.1)


if __name__ == "__main__":
    unittest.main()
