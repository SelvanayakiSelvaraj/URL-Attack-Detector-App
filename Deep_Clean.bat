@echo off
echo =========================================
echo   URL ATTACK DETECTOR - DEEP CLEANUP
echo =========================================
echo.
echo Searching and destroying temporary files to save storage space...
echo.

echo [1/4] Destroying Temporary Troubleshooting Scripts...
del /f /q Show_Error.bat 2>nul
del /f /q check_compile.bat 2>nul
del /f /q hard_rebuild.bat 2>nul
del /f /q compile_maven.js 2>nul

echo [2/4] Destroying Temporary Diagnostic Logs...
del /f /q compile._log.txt 2>nul
del /f /q history_debug.txt 2>nul
del /f /q url_debug.txt 2>nul
del /f /q read_log.py 2>nul

echo [3/4] Destroying Massive Electron Developer Folders...
echo ^(This wipes the uncompressed cache and frees ~400MB^)
rmdir /s /q desktop_app\dist 2>nul
rmdir /s /q desktop_app\release\win-unpacked 2>nul

echo [4/4] Destroying Java Class Output Folders...
rmdir /s /q target\classes 2>nul
rmdir /s /q target\test-classes 2>nul
rmdir /s /q target\generated-sources 2>nul
rmdir /s /q target\maven-status 2>nul

echo.
echo =========================================
echo   DEEP CLEANUP COMPLETE! 
echo   Hundreds of Megabytes safely deleted!
echo   (Your final .exe installer remains safe in "release")
echo =========================================
echo Press any key to close...
pause >nul
