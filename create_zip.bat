@echo off
setlocal
set SOURCE=%~dp0
set TEMP_DIR=%TEMP%\url_detector_pkg
set ZIP_FILE=%USERPROFILE%\Desktop\URL_Attack_Detector_Project.zip

echo ====================================================
echo   URL Attack Detector - College Submission Zip
echo ====================================================
echo.

echo [1/4] Cleaning up existing files...
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"
if exist "%ZIP_FILE%" del /f /q "%ZIP_FILE%"

echo [2/4] Creating a clean folder for submission...
mkdir "%TEMP_DIR%"
xcopy "%SOURCE%" "%TEMP_DIR%" /e /i /h /y > nul

echo [3/4] Removing large non-essential folders (Target, Node_Modules, etc)...
rd /s /q "%TEMP_DIR%\.git" 2>nul
rd /s /q "%TEMP_DIR%\target" 2>nul
rd /s /q "%TEMP_DIR%\desktop_app\node_modules" 2>nul
rd /s /q "%TEMP_DIR%\desktop_app\dist" 2>nul
rd /s /q "%TEMP_DIR%\desktop_app\dist_new" 2>nul
rd /s /q "%TEMP_DIR%\desktop_app\release" 2>nul
rd /s /q "%TEMP_DIR%\ml_service\venv" 2>nul
rd /s /q "%TEMP_DIR%\.settings" 2>nul
del /f /q "%TEMP_DIR%\.classpath" 2>nul
del /f /q "%TEMP_DIR%\.project" 2>nul
del /f /q "%TEMP_DIR%\*.zip" 2>nul
del /f /q "%TEMP_DIR%\*.log" 2>nul

echo [4/4] Compressing into Zip file using tar...
cd /d "%TEMP_DIR%"
tar -a -c -f "%ZIP_FILE%" *

echo.
echo ====================================================
echo SUCCESS!
echo Your zip file is ready at: %ZIP_FILE%
echo ====================================================
echo.
pause
rd /s /q "%TEMP_DIR%"
