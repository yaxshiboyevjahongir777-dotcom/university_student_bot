@echo off
:loop
cd /d "C:\Users\Jahongir MT\Desktop\university_bot"
echo [%date% %time%] Bot ishga tushirilmoqda...
py main.py
echo [%date% %time%] Bot to'xtadi. 5 soniyadan keyin qayta yoqiladi...
timeout /t 5
goto loop