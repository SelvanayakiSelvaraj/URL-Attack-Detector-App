@echo off
setlocal
echo =========================================
echo   Starting URL Attack Detector Services
echo =========================================
echo.

echo [Step 1] Clearing port 8080 (if in use)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /R /C:":8080 "') do (
    echo [INFO] Found process %%a on port 8080, attempting to close it...
    taskkill /f /pid %%a >nul 2>&1
)

echo [Step 2] Starting Machine Learning API Service...
start "URL Detector - ML Service" cmd /k "cd ml_service && python -m venv venv && venv\Scripts\activate.bat && pip install -r requirements.txt && python train_model.py && python app.py"

echo [Step 3] Starting Spring Boot Backend...
start "URL Detector - Spring Backend" cmd /k "mvnw.cmd spring-boot:run"

echo.
echo =========================================
echo   SERVICES ARE STARTING
echo =========================================
echo.
echo Please wait about 10 seconds for the servers to warm up...
timeout /t 10 /nobreak >nul
echo Launching Application UI...
start http://localhost:8080/
echo.
echo 1. Keep the other two black windows open while using the app.
echo 2. If the page doesn't load yet, just refresh (F5) in a few seconds.
echo.
echo Press any key to close this launcher...
pause >nul

