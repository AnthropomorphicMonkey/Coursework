@echo off
echo Compile?
pause
file_prep.py
pyinstaller main.py -F -n MathsQuiz -w -i icon.ico
echo Success
pause