@echo off

call %~dp0telegram_bot\venv\Scripts\activate

cd %~dp0telegram_bot

set TOKEN=5038604764:AAH8PRxN77d5UDG_6KVvon1nw3WrYzkj0wY

python main.py

pause