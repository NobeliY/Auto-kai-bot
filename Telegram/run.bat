@echo off
call "%~dp0Telegram\venv\Scripts\activate"
cd "%~dp0tg_bot"
python app.py
