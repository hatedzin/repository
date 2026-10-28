@echo off
setlocal
cd /d "%~dp0"
title Sdds cheats - Criar administrador
echo Este assistente cria a conta admin. Nao existe senha padrao.
echo Se a conta ja existir, ela sera preservada.
call start.bat --create-admin admin
set "sdds_exit=%errorlevel%"
pause
exit /b %sdds_exit%
