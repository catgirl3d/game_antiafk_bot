import sys
import types
import unittest
from unittest.mock import patch


fake_pyautogui = types.ModuleType('pyautogui')
fake_pyautogui.keyDown = lambda *args, **kwargs: None
fake_pyautogui.keyUp = lambda *args, **kwargs: None
fake_pyautogui.moveRel = lambda *args, **kwargs: None
fake_pyautogui.click = lambda *args, **kwargs: None
sys.modules.setdefault('pyautogui', fake_pyautogui)

from core.bot import AntiAfkBot


class BotStatusTests(unittest.TestCase):
    def setUp(self):
        self.bot = AntiAfkBot()

    @patch('core.bot.time.time', return_value=105.0)
    def test_get_status_uses_backend_schedule(self, _mock_time):
        self.bot.running = True
        self.bot.phase = 'waiting'
        self.bot.started_at = 100.0
        self.bot.interval_started_at = 100.0
        self.bot.current_interval = 10.0
        self.bot.next_action_at = 110.0
        self.bot.action_count = 3

        status = self.bot.get_status()

        self.assertTrue(status['running'])
        self.assertEqual(status['phase'], 'waiting')
        self.assertEqual(status['action_count'], 3)
        self.assertEqual(status['current_interval_seconds'], 10.0)
        self.assertEqual(status['remaining_seconds'], 5.0)
        self.assertAlmostEqual(status['progress'], 0.5)

    @patch('core.bot.time.time', return_value=205.0)
    def test_get_status_clears_timer_when_action_is_running(self, _mock_time):
        self.bot.running = True
        self.bot.phase = 'acting'
        self.bot.started_at = 200.0
        self.bot.action_count = 7

        status = self.bot.get_status()

        self.assertTrue(status['running'])
        self.assertEqual(status['phase'], 'acting')
        self.assertEqual(status['action_count'], 7)
        self.assertIsNone(status['current_interval_seconds'])
        self.assertEqual(status['remaining_seconds'], 0.0)
        self.assertEqual(status['progress'], 1.0)


if __name__ == '__main__':
    unittest.main()
