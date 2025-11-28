@echo off
title XAMPP Database Server Launcher
echo ========================================
echo    XAMPP Database Server Launcher
echo ========================================
echo.

REM Stop any running XAMPP processes first
echo [1/6] Stopping any existing XAMPP processes...
taskkill /F /IM httpd.exe >nul 2>&1
taskkill /F /IM mysqld.exe >nul 2>&1
timeout /t 2 >nul

REM Backup original configurations if not already done
echo [2/6] Backing up configurations...
if not exist "C:\xampp\mysql\bin\my.ini.backup" (
    copy "C:\xampp\mysql\bin\my.ini" "C:\xampp\mysql\bin\my.ini.backup" >nul 2>&1
)
if not exist "C:\xampp\apache\conf\httpd.conf.backup" (
    copy "C:\xampp\apache\conf\httpd.conf" "C:\xampp\apache\conf\httpd.conf.backup" >nul 2>&1
)

REM Configure MySQL to use port 3307 (to avoid conflict with existing MySQL on 3306)
echo [3/6] Configuring MySQL for port 3307...
powershell -Command "(Get-Content 'C:\xampp\mysql\bin\my.ini') -replace 'port\s*=\s*3306', 'port=3307' | Set-Content 'C:\xampp\mysql\bin\my.ini'"

REM Configure phpMyAdmin for port 3307
echo [4/6] Configuring phpMyAdmin...
powershell -Command "if (Test-Path 'C:\xampp\phpMyAdmin\config.inc.php') { (Get-Content 'C:\xampp\phpMyAdmin\config.inc.php') -replace \"\\$cfg\\['Servers'\\]\\[\\$i\\]\\['port'\\] = '3306';\", \"\\$cfg['Servers'][\\$i]['port'] = '3307';\" | Set-Content 'C:\xampp\phpMyAdmin\config.inc.php' }"

REM Start XAMPP Control Panel
echo [5/6] Starting XAMPP Control Panel...
start "" "C:\xampp\xampp-control.exe"
timeout /t 3 >nul

REM Instructions
echo [6/6] Setup Complete!
echo.
echo ========================================
echo    NEXT STEPS:
echo ========================================
echo 1. In the XAMPP Control Panel that just opened:
echo    - Click START next to MySQL
echo    - Click START next to Apache
echo.
echo 2. Once both services show "Running":
echo    - Open: http://localhost/phpmyadmin
echo    - Access your database management interface
echo.
echo 3. Your Django database dashboard is also available at:
echo    - http://127.0.0.1:8000/database-dashboard/
echo.
echo ========================================
echo    PORT CONFIGURATION:
echo ========================================
echo - Existing MySQL (Django): Port 3306
echo - XAMPP MySQL (phpMyAdmin): Port 3307  
echo - Apache (Web Server): Port 80
echo.
echo Press any key when done...
pause >nul