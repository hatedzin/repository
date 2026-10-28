@echo off
setlocal
cd /d "%~dp0"
title Sdds cheats - Administrador
echo Painel ADMINISTRATIVO: usa conta e senha para proteger suas keys.
echo Primeiro acesso? Execute configurar-admin.cmd para criar a conta admin.
echo Para entrar SOMENTE COM KEY, abra usuario.cmd.
if not exist ".venv\Scripts\python.exe" (
    echo Execute start.bat primeiro para preparar e iniciar o servidor.
    pause
    exit /b 1
)
.venv\Scripts\python.exe terminal.py --admin
set "sdds_exit=%errorlevel%"
pause
exit /b %sdds_exit%
