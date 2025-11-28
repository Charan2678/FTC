@echo off
title Stop XAMPP Services
echo ========================================
echo      Stopping XAMPP Services
echo ========================================
echo.

echo Stopping Apache and MySQL services...
taskkill /F /IM httpd.exe >nul 2>&1
taskkill /F /IM mysqld.exe >nul 2>&1

echo Closing XAMPP Control Panel...
taskkill /F /IM xampp-control.exe >nul 2>&1

echo.
echo All XAMPP services have been stopped.
echo Your Django server (if running) remains active.
echo.
timeout /t 3 >nul