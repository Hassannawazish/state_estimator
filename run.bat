@echo off

REM open a new console window for each script:
start "" python evaluate_ekf.py
start "" python evaluate_pf.py
start "" python localization.py --plot pf

REM optional: exit this “launcher” window
exit
