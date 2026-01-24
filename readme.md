# 🤖 Anti-AFK Bot

[English](readme.md) | [Українська](README_UA.md) | [Русский](README_RU.md)

**Anti-AFK Bot** is a simple and elegant solution to prevent automatic disconnection (AFK) in games and applications. Built with Python and modern web technologies for the interface.

[![Latest Release](https://img.shields.io/github/v/release/catgirl3d/game_antiafk_bot?style=flat-square&label=Download&color=success)](https://github.com/catgirl3d/game_antiafk_bot/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://www.python.org/)

## ✨ Features

- **Easy Setup**: Enter the key, set the interval, and you're good to go.
- **Autosave**: Remembers your settings and window position.
- **Stats**: Shows the number of presses and active time.
- **Always on Top**: Can be pinned above other windows.
- **Minimalist**: Small window without extra borders.

## 🛠 Tech Stack

- **Core**: Python 3.10+, `pyautogui`, `pywebview`.
- **UI**: HTML5, CSS3 (Vanilla), JavaScript (Vanilla).
- **Build**: PyInstaller, GitHub Actions.

## 🚀 Quick Start

### From source code:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/catgirl3d/game_antiafk_bot.git
   cd game_antiafk_bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run**:
   ```bash
   python main.py
   ```

## 📦 Build EXE

The project is configured for automatic builds via **GitHub Actions**. Creating a new tag (e.g., `v1.0.0`) automatically creates a Release with the `.exe` file.

### Local build:

If you want to build the executable yourself:

```bash
pyinstaller --clean --noconfirm game_antiafk_bot.spec
```

The result will appear in the `dist/` folder.

## ⚙️ Key Configuration

The bot supports both single characters and special keys:
- `space`, `f1`, `f12`, `shift`, `ctrl`, `alt`, `enter`, etc.
- Full list of supported names matches the [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys) library.
