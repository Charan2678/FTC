@echo off
title Quick Database Access
echo ========================================
echo        Quick Database Access
echo ========================================
echo.
echo Choose your database interface:
echo.
echo [1] phpMyAdmin (Web-based MySQL interface)
echo [2] Django Database Dashboard  
echo [3] Both interfaces
echo [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Opening phpMyAdmin...
    start "" "http://localhost/phpmyadmin"
) else if "%choice%"=="2" (
    echo Opening Django Database Dashboard...
    start "" "http://127.0.0.1:8000/database-dashboard/"
) else if "%choice%"=="3" (
    echo Opening both interfaces...
    start "" "http://localhost/phpmyadmin"
    timeout /t 2 >nul
    start "" "http://127.0.0.1:8000/database-dashboard/"
) else if "%choice%"=="4" (
    exit
) else (
    echo Invalid choice. Please try again.
    timeout /t 2 >nul
    goto :eof
)

echo.
echo Database interfaces opened successfully!
timeout /t 3 >nul