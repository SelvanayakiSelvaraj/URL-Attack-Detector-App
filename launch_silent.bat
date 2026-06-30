@echo off
echo =========================================
echo   URL ATTACK DETECTOR - SILENT MODE
echo =========================================
echo.
echo [1/3] Clearing port 8080...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1

echo [2/3] Starting AI & Backend Engines HIDEEN...

:: Start ML Service Hidden
powershell -Command "Start-Process python -ArgumentList 'ml_service/app.py' -WindowStyle Hidden -WorkingDirectory '%cd%'"

:: Start Spring Backend Hidden
powershell -Command "Start-Process cmd -ArgumentList '/c mvnw.cmd spring-boot:run' -WindowStyle Hidden -WorkingDirectory '%cd%'"

echo [3/3] Warming up engines (20 seconds)...
timeout /t 20 /nobreak >nul

echo.
echo Launching Dashboard...
start http://localhost:8080/

echo.
echo =========================================
echo   APP IS NOW RUNNING IN BACKGROUND
echo =========================================
echo To STOP the app later, run: stop_detector.bat
echo.
timeout /t 5 /nobreak >nul
exit
