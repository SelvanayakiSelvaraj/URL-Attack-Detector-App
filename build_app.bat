@echo off
echo =========================================
echo   Building URL Attack Detector App
echo =========================================
echo.

echo [1/3] Terminating ALL hidden background servers and Code Editors...
taskkill /F /IM java.exe /T 2>nul
taskkill /F /IM javaw.exe /T 2>nul
taskkill /F /IM Code.exe /T 2>nul
taskkill /F /IM eclipse.exe /T 2>nul
taskkill /F /IM idea64.exe /T 2>nul
taskkill /F /IM electron.exe /T 2>nul
wmic process where "name like '%%java%%'" delete 2>nul
echo Cleaning corrupted build directories...
del /f /s /q desktop_app\dist\* 2>nul
rmdir /s /q desktop_app\dist 2>nul
echo.

echo [2/3] Compiling Java Spring Boot Backend into a Standalone JAR...
call mvnw.cmd package -DskipTests

echo.
echo [3/4] Setting up Desktop App Environment...
cd desktop_app
call npm install electron electron-builder

echo.
echo [4/4] Packaging into a Standalone Windows .exe...
call .\node_modules\.bin\electron-builder.cmd --win > build_log.txt 2>&1

echo.
echo =========================================
echo   Build Complete!
echo =========================================
echo You can find your new installer app inside:
echo desktop_app/dist/url-attack-detector Setup 1.0.0.exe
echo.
pause
