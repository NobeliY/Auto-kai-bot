@echo off
call "%~dp0Auto-kai-bot\Telegram\venv\Scripts\activate"
cd "%~dp0tg_bot"
python app.py
