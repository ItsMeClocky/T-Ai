@echo off
REM T-Ai Installer for Windows
echo Installing T-Ai...
echo This will create a desktop shortcut for T-Ai

set SHORTCUT_PATH=%USERPROFILE%\Desktop\T-Ai.url
set TARGET_URL=http://localhost:8080/index.html

echo [InternetShortcut] > "%SHORTCUT_PATH%"
echo URL=%TARGET_URL% >> "%SHORTCUT_PATH%"
echo IconIndex=0 >> "%SHORTCUT_PATH%"

echo T-Ai installed! Check your desktop for the shortcut.
echo Note: Make sure the backend server is running: python3 api_keys.py
pause
