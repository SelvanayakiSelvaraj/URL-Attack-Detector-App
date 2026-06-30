@echo off
echo =========================================
echo   STOPPING URL ATTACK DETECTOR
echo =========================================

:: Kill Java (Spring Boot)
echo Stopping Spring Backend...
taskkill /f /im java.exe /t >nul 2>&1

:: Kill Python (ML Service)
echo Stopping ML Service...
taskkill /f /im python.exe /t >nul 2>&1

echo.
echo All services stopped successfully!
timeout /t 3 /nobreak >nul
exit
