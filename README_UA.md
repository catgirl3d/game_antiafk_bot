# 🤖 Anti-AFK Bot

[English](readme.md) | [Українська](README_UA.md) | [Русский](README_RU.md)

**Anti-AFK Bot** — це просте рішення для запобігання автоматичному відключенню (AFK) в іграх та програмах. Написаний на Python з використанням сучасних веб-технологій для інтерфейсу.

[![Latest Release](https://img.shields.io/github/v/release/catgirl3d/game_antiafk_bot?style=flat-square&label=Download&color=success)](https://github.com/catgirl3d/game_antiafk_bot/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://www.python.org/)

## ✨ Можливості

- **Просте налаштування**: Ввів клавішу, поставив інтервал і готово.
- **Автозбереження**: Запам'ятовує налаштування та положення вікна.
- **Статистика**: Показує кількість натискань та час роботи.
- **Поверх вікон**: Можна закріпити вікно поверх інших.
- **Мінімалізм**: Маленьке вікно без зайвих рамок.

## 🛠 Технологічний стек

- **Core**: Python 3.10+, `pyautogui`, `pywebview`.
- **UI**: HTML5, CSS3 (Vanilla), JavaScript (Vanilla).
- **Build**: PyInstaller, GitHub Actions.

## 🚀 Швидкий запуск

### З вихідного коду:

1. **Клонуйте репозиторій**:
   ```bash
   git clone https://github.com/catgirl3d/game_antiafk_bot.git
   cd game_antiafk_bot
   ```

2. **Встановіть залежності**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Запустіть**:
   ```bash
   python main.py
   ```

## 📦 Збірка в EXE

Проєкт налаштований на автоматичну збірку через **GitHub Actions**. При створенні нового тегу (наприклад, `v1.0.0`) автоматично створюється Release з готовим `.exe` файлом.

### Локальна збірка:

Якщо ви хочете зібрати виконуваний файл самостійно:

```bash
pyinstaller --clean --noconfirm game_antiafk_bot.spec
```

Результат з'явиться в папці `dist/`.

## ⚙️ Налаштування клавіш

Бот підтримує як поодинокі символи, так і спеціальні клавіші:
- `space`, `f1`, `f12`, `shift`, `ctrl`, `alt`, `enter` та ін.
- Повній список підтримуваних назв відповідає бібліотеці [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys).
