@echo off
echo.
echo ============================================================
echo   URL ATTACK DETECTOR - AUTOMATED REBUILD SYSTEM
echo ============================================================
echo.

echo [1/5] Forcefully closing any running instances...
taskkill /IM "URL Attack Detector App.exe" /F 2>nul
taskkill /IM java.exe /F 2>nul
taskkill /IM python.exe /F 2>nul
timeout /t 2 /nobreak >nul

echo [2/5] Re-compiling Java Backend (Creating fresh JAR)...
cd ..
call mvnw package -DskipTests
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Java build failed! Please check your code.
    pause
    exit /b %ERRORLEVEL%
)

echo [3/5] Re-training Machine Learning AI (Expanding Brain)...
cd ml_service
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt > nul
python train_model.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] AI Training failed!
    pause
    exit /b %ERRORLEVEL%
)
call venv\Scripts\deactivate.bat

echo [4/5] Packaging everything into a new Windows Installer...
cd ..\desktop_app
call npm run dist
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Electron packaging failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ============================================================
echo   SUCCESS! Your new enhanced app is ready in:
echo   desktop_app\release
echo ============================================================
echo.
pause
