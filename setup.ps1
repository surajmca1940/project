# IndAid Mental Health Platform - PowerShell Setup Script
# Version 1.0

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "   IndAid - Mental Health Support Platform" -ForegroundColor Green  
Write-Host "             Setup Script v1.0" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-CommandExists {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# Step 1: Check Python installation
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
if (Test-CommandExists "python") {
    $pythonVersion = python --version 2>$null
    Write-Host "$pythonVersion found successfully!" -ForegroundColor Green
} else {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Step 2: Create virtual environment
Write-Host "[2/6] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists, skipping..." -ForegroundColor Yellow
} else {
    try {
        python -m venv venv
        Write-Host "Virtual environment created successfully!" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}
Write-Host ""

# Step 3: Activate virtual environment
Write-Host "[3/6] Activating virtual environment..." -ForegroundColor Yellow
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "Virtual environment activated!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "You may need to change PowerShell execution policy:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Step 4: Upgrade pip
Write-Host "[4/6] Upgrading pip..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip | Out-Null
    Write-Host "pip upgraded successfully!" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Failed to upgrade pip, continuing..." -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Install dependencies
Write-Host "[5/6] Installing project dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes, please wait..." -ForegroundColor Cyan
try {
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Dependencies installed successfully!" -ForegroundColor Green
    } else {
        throw "pip install failed"
    }
} catch {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Write-Host "Please check your internet connection and try again" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Step 6: Setup Django database
Write-Host "[6/6] Setting up Django database..." -ForegroundColor Yellow
try {
    Write-Host "Creating migrations..." -ForegroundColor Cyan
    python manage.py makemigrations
    if ($LASTEXITCODE -ne 0) { throw "makemigrations failed" }
    
    Write-Host "Applying migrations..." -ForegroundColor Cyan
    python manage.py migrate
    if ($LASTEXITCODE -ne 0) { throw "migrate failed" }
    
    Write-Host "Database setup complete!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to setup database" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Bonus: Collect static files
Write-Host "[BONUS] Collecting static files..." -ForegroundColor Yellow
try {
    python manage.py collectstatic --noinput | Out-Null
    Write-Host "Static files collected!" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Failed to collect static files, but project should still work" -ForegroundColor Yellow
}
Write-Host ""

# Success message
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "          SETUP COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your IndAid Mental Health Platform is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the development server, run:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Cyan
Write-Host ""
Write-Host "Then open your browser and go to:" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "To create an admin user (optional):" -ForegroundColor White
Write-Host "   python manage.py createsuperuser" -ForegroundColor Cyan
Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "          Happy Coding! 🎉" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to continue"
