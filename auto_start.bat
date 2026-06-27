@echo off
setlocal

set "APP_NAME=PC Text Input Server"
set "PROJECT_DIR=%~dp0"

:: Remove trailing backslash
if "%PROJECT_DIR:~-1%"=="\" set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"

:: Create launcher
(
echo @echo off
echo cd /d "%PROJECT_DIR%"
echo uv run run.py
) > "%PROJECT_DIR%\run_server.cmd"

:: Create hidden launcher in Startup folder
set "STARTUP_VBS=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\%APP_NAME%.vbs"

(
echo Set WshShell = CreateObject("WScript.Shell"^)
echo WshShell.CurrentDirectory = "%PROJECT_DIR%"
echo WshShell.Run """%PROJECT_DIR%\run_server.cmd""", 0, False
) > "%STARTUP_VBS%"

echo.
echo Installed successfully in Startup folder.
echo The server will start automatically after you log in.

:: Start it now in the background
start "" /B wscript.exe "%STARTUP_VBS%"

echo Server started.
pause