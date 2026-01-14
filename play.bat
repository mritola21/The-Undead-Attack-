@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting The Undead Attack!
python run_game.py
pause