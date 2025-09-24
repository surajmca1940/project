#!/bin/bash

# IndAid Mental Health Platform - Linux/macOS Setup Script
# Version 1.0

echo "==============================================="
echo "   IndAid - Mental Health Support Platform"
echo "             Setup Script v1.0 (Linux/macOS)"
echo "==============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Step 1: Check Python installation
print_step "[1/7] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_status "$PYTHON_VERSION found successfully!"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    if [[ $PYTHON_VERSION == *"Python 3"* ]]; then
        print_status "$PYTHON_VERSION found successfully!"
        PYTHON_CMD="python"
    else
        print_error "Python 3 required, but found $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python is not installed"
    echo "Please install Python 3.8+ using your package manager:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi
echo ""

# Step 2: Check pip installation
print_step "[2/7] Checking pip installation..."
if command -v pip3 &> /dev/null; then
    print_status "pip3 found successfully!"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    print_status "pip found successfully!"
    PIP_CMD="pip"
else
    print_error "pip is not installed"
    echo "Please install pip using your package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3-pip"
    exit 1
fi
echo ""

# Step 3: Create virtual environment
print_step "[3/7] Creating virtual environment..."
if [ -d "venv" ] || [ -d "env" ]; then
    print_warning "Virtual environment already exists, skipping..."
else
    $PYTHON_CMD -m venv env
    if [ $? -eq 0 ]; then
        print_status "Virtual environment created successfully!"
    else
        print_error "Failed to create virtual environment"
        echo "Try installing python3-venv: sudo apt install python3-venv"
        exit 1
    fi
fi
echo ""

# Step 4: Activate virtual environment
print_step "[4/7] Activating virtual environment..."
if [ -f "env/bin/activate" ]; then
    source env/bin/activate
    print_status "Virtual environment activated!"
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    print_status "Virtual environment activated!"
else
    print_error "Virtual environment activation script not found"
    exit 1
fi
echo ""

# Step 5: Upgrade pip
print_step "[5/7] Upgrading pip..."
python -m pip install --upgrade pip
if [ $? -eq 0 ]; then
    print_status "pip upgraded successfully!"
else
    print_warning "Failed to upgrade pip, continuing..."
fi
echo ""

# Step 6: Install dependencies
print_step "[6/7] Installing project dependencies..."
echo "This may take a few minutes, please wait..."
if [ -f "requirements.txt" ]; then
    python -m pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_status "Dependencies installed successfully!"
    else
        print_error "Failed to install dependencies"
        echo "Please check your internet connection and try again"
        echo "You can also try installing manually:"
        echo "  python -m pip install django django-admin-interface pillow google-generativeai"
        exit 1
    fi
else
    print_error "requirements.txt not found"
    echo "Installing essential packages manually..."
    python -m pip install django django-admin-interface django-colorfield pillow google-generativeai pydantic requests
fi
echo ""

# Step 7: Setup Django database
print_step "[7/7] Setting up Django database..."
if [ -f "manage.py" ]; then
    print_status "Creating migrations..."
    python manage.py makemigrations
    if [ $? -ne 0 ]; then
        print_warning "makemigrations failed, but continuing..."
    fi
    
    print_status "Applying migrations..."
    python manage.py migrate
    if [ $? -eq 0 ]; then
        print_status "Database setup complete!"
    else
        print_error "Failed to apply migrations"
        exit 1
    fi
else
    print_error "manage.py not found"
    echo "Make sure you're in the correct project directory"
    exit 1
fi
echo ""

# Bonus: Collect static files
print_step "[BONUS] Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -eq 0 ]; then
    print_status "Static files collected!"
else
    print_warning "Failed to collect static files, but project should still work"
fi
echo ""

# Success message
echo "==============================================="
echo -e "${GREEN}          SETUP COMPLETED SUCCESSFULLY!${NC}"
echo "==============================================="
echo ""
echo -e "${GREEN}Your IndAid Mental Health Platform is ready!${NC}"
echo ""
echo -e "${BLUE}To start the development server, run:${NC}"
echo -e "${YELLOW}   python manage.py runserver${NC}"
echo ""
echo -e "${BLUE}Then open your browser and go to:${NC}"
echo -e "${YELLOW}   http://127.0.0.1:8000${NC}"
echo ""
echo -e "${BLUE}To create an admin user (optional):${NC}"
echo -e "${YELLOW}   python manage.py createsuperuser${NC}"
echo ""
echo -e "${BLUE}To activate virtual environment in future:${NC}"
echo -e "${YELLOW}   source env/bin/activate${NC}"
echo ""
echo "==============================================="
echo -e "${GREEN}          Happy Coding! 🎉${NC}"
echo "==============================================="
echo ""

# Keep terminal open
read -p "Press Enter to continue..."
