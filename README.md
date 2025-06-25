# Telegram Animated Text Bot

This repository contains a Telegram bot built with the [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) library and a minimal Django project for storing message data. The bot replies to `/start` and `/help` commands and supports inline message animations.

## Requirements
- Python 3.13+
- MySQL
- Libraries `Django`, `mysqlclient`, `Pillow`, `pyTelegramBotAPI`
- Additional libraries can be found in the [telegram_bot_core](https://github.com/NGGTLightKeeper/telegram_bot_core) repository

## Installation
1. Create and activate a virtual environment.
2. Install the dependencies:
   ```bash
   pip install Django mysqlclient Pillow pyTelegramBotAPI
   ```
3. Configure the database connection in `settings/settings.py`.
4. Apply migrations:
   ```bash
   python main.py makemigrations
   python main.py migrate
   ```
5. Run the bot:
   ```bash
   python main.py runserver
   ```

## Project Structure
- `bot.py` – Telegram bot logic
- `telegram_bot_django/` – Django project settings
- `telegram_bot_db/` – Django application with models and tests
- `messages/` – text files with greeting and help messages

## License
This project is licensed under the [MIT License](LICENSE).
