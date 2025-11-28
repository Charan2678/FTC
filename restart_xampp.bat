@echo off
echo Stopping XAMPP services...
taskkill /F /IM httpd.exe >nul 2>&1
taskkill /F /IM mysqld.exe >nul 2>&1

echo Starting XAMPP Control Panel...
start "" "C:\xampp\xampp-control.exe"

echo.
echo Please use the XAMPP Control Panel to start:
echo 1. MySQL service
echo 2. Apache service
echo.
echo Then open: http://localhost/phpmyadmin
pause