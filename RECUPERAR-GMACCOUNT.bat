@echo off
setlocal
set "ASTRO_RECOVERY_ROOT=%~dp0"
if exist "%ASTRO_RECOVERY_ROOT%DisneyClient\manage_accounts.py" goto found
set "ASTRO_RECOVERY_ROOT=%~dp0DisneyClient-Local-Robot-Novo\"
if exist "%ASTRO_RECOVERY_ROOT%DisneyClient\manage_accounts.py" goto found
echo Coloque este arquivo ao lado do INICIAR_TUDO.bat da instalacao que voce usa.
echo O projeto precisa estar extraido e preparado.
pause
exit /b 1
:found
set "ASTRO_RECOVERY_PY=%ASTRO_RECOVERY_ROOT%.client-runtime\Scripts\python.exe"
if not exist "%ASTRO_RECOVERY_PY%" (
 echo O Python local do client nao foi encontrado.
 echo Execute INICIAR_TUDO.bat nesta instalacao primeiro e tente novamente.
 pause
 exit /b 1
)
echo Recuperacao local da conta gmaccount.
echo Mantenha o MySQL do XAMPP ligado.
echo Digite uma senha temporaria de 12 a 128 caracteres e confirme.
echo A digitacao da senha fica oculta. A senha nao sera exibida.
echo.
pushd "%ASTRO_RECOVERY_ROOT%DisneyClient"
if errorlevel 1 exit /b 1
"%ASTRO_RECOVERY_PY%" manage_accounts.py reset-password gmaccount
set "ASTRO_RECOVERY_RESULT=%errorlevel%"
popd
if "%ASTRO_RECOVERY_RESULT%"=="0" (
 echo.
 echo Senha redefinida. Entre no site como gmaccount usando a senha que escolheu.
 echo No primeiro acesso, o site pedira outra troca de senha.
) else (
 echo.
 echo A recuperacao nao foi concluida. Confira a mensagem acima e o MySQL.
)
pause
exit /b %ASTRO_RECOVERY_RESULT%
