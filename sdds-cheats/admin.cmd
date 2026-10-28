@echo off
setlocal
cd /d "%~dp0"
title Sdds cheats - Administrador
if not exist ".venv\Scripts\python.exe" (
    echo Execute start.bat primeiro para preparar e iniciar o servidor.
    pause
    exit /b 1
)
.venv\Scripts\python.exe terminal.py --admin
set "sdds_exit=%errorlevel%"
pause
exit /b %sdds_exit%
