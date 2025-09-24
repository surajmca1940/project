@echo off
title IndAid Mental Health Platform - Setup
color 0A

echo ===============================================
echo    IndAid - Mental Health Support Platform
echo              Setup Script v1.0
echo ===============================================
echo.

echo [1/6] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
) else (
    python --version
    echo Python found successfully!
)
echo.

echo [2/6] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)
echo.

echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

echo [4/6] Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo WARNING: Failed to upgrade pip, continuing...
)
echo.

echo [5/6] Installing project dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [6/6] Setting up Django database...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo ERROR: Failed to create migrations
    pause
    exit /b 1
)

python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to apply migrations
    pause
    exit /b 1
)
echo Database setup complete!
echo.

echo [BONUS] Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo WARNING: Failed to collect static files, but project should still work
)
echo Static files collected!
echo.

echo ===============================================
echo           SETUP COMPLETED SUCCESSFULLY!
echo ===============================================
echo.
echo Your IndAid Mental Health Platform is ready!
echo.
echo To start the development server, run:
echo    python manage.py runserver
echo.
echo Then open your browser and go to:
echo    http://127.0.0.1:8000
echo.
echo To create an admin user (optional):
echo    python manage.py createsuperuser
echo.
echo ===============================================
echo           Happy Coding! 🎉
echo ===============================================
echo.
pause
