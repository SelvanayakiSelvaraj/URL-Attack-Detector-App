@echo off
echo =========================================
echo   ANTIGRAVITY INSTALLER CLEANUP WIZARD
echo =========================================
echo.
echo Deleting old installer files from your Desktop to free up ~345 MB...
echo.

del /f /q "%USERPROFILE%\OneDrive\Desktop\Antigravity (1).exe" 2>nul
del /f /q "%USERPROFILE%\OneDrive\Desktop\Antigravity.exe" 2>nul

echo Done! The massive installer files are gone.
echo You can check your Desktop - only the shortcut remains!
echo =========================================
pause
