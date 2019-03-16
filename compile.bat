@echo off
echo Compile?
pause
file_prep.py
pyinstaller main.py -w --onefile
echo Success
pause