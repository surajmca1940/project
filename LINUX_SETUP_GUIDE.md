# 🐧 IndAid - Linux Setup Guide

## 🚨 **Quick Fix for "No module named 'admin_interface'" Error**

If you're getting the error `ModuleNotFoundError: No module named 'admin_interface'`, follow these steps:

### **Immediate Solution:**
```bash
# 1. Activate virtual environment
source env/bin/activate  # or source venv/bin/activate

# 2. Install missing dependencies
pip install django-admin-interface django-colorfield

# 3. Install all project dependencies
pip install -r requirements.txt

# 4. Run the server
python manage.py runserver
```

---

## 🛠️ **Complete Linux Setup Instructions**

### **Prerequisites for Ubuntu/Debian:**
```bash
# Update package list
sudo apt update

# Install Python 3 and essential packages
sudo apt install python3 python3-pip python3-venv git

# Install development tools (optional but recommended)
sudo apt install build-essential python3-dev
```

### **Prerequisites for CentOS/RHEL/Fedora:**
```bash
# CentOS/RHEL
sudo yum install python3 python3-pip git

# Fedora
sudo dnf install python3 python3-pip git
```

### **Prerequisites for macOS:**
```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Git
brew install python3 git
```

---

## 🚀 **Automated Setup (Recommended)**

### **Method 1: Use the Linux Setup Script**
```bash
# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

### **Method 2: Manual Setup**
```bash
# 1. Create virtual environment
python3 -m venv env

# 2. Activate virtual environment
source env/bin/activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Setup database
python manage.py makemigrations
python manage.py migrate

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Run server
python manage.py runserver
```

---

## 🔧 **Troubleshooting Common Linux Issues**

### **1. "No module named 'admin_interface'"**
```bash
# Install missing Django packages
pip install django-admin-interface django-colorfield

# If that doesn't work, reinstall all dependencies
pip install --force-reinstall -r requirements.txt
```

### **2. "python3: command not found"**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3

# CentOS/RHEL
sudo yum install python3

# Check installation
python3 --version
```

### **3. "pip: command not found"**
```bash
# Ubuntu/Debian
sudo apt install python3-pip

# CentOS/RHEL
sudo yum install python3-pip

# Alternative: install using get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### **4. "No module named 'venv'"**
```bash
# Ubuntu/Debian
sudo apt install python3-venv

# Then try creating virtual environment again
python3 -m venv env
```

### **5. Permission Denied Errors**
```bash
# Make sure you're not using sudo with pip in virtual environment
# Always activate virtual environment first
source env/bin/activate

# Then install packages without sudo
pip install -r requirements.txt
```

### **6. "Port already in use" (Linux/macOS)**
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill the process (replace PID with actual process ID)
kill -9 PID

# Or use a different port
python manage.py runserver 8001
```

### **7. Database Locked Error**
```bash
# Stop any running Django processes
pkill -f "python manage.py runserver"

# Remove database lock (if SQLite)
rm db.sqlite3

# Recreate database
python manage.py migrate

# Create superuser again
python manage.py createsuperuser
```

### **8. Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check if static directory exists
ls -la static/

# If not, create it
mkdir -p static/css static/js
```

---

## 📋 **Linux-Specific Requirements File**

Create a `requirements-linux.txt` file if you have Linux-specific dependencies:

```txt
# Core Django
Django==5.2.6
django-admin-interface==0.30.1
django-colorfield==0.14.0

# AI and APIs
google-generativeai==0.8.5
google-api-python-client==2.182.0

# Image processing
Pillow==11.3.0

# Data validation
pydantic==2.11.9

# HTTP requests
requests==2.32.5

# Other utilities
python-slugify==8.0.4
tqdm==4.67.1

# Linux-specific packages (if needed)
# psycopg2-binary  # For PostgreSQL on Linux
# gunicorn         # For production deployment
```

---

## 🐳 **Docker Setup (Alternative)**

If you're having persistent dependency issues, use Docker:

### **Create Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### **Create docker-compose.yml:**
```yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=True
```

### **Run with Docker:**
```bash
# Build and run
docker-compose up --build

# Or run without docker-compose
docker build -t indaid .
docker run -p 8000:8000 indaid
```

---

## 📱 **Virtual Environment Management**

### **Activation Commands:**
```bash
# Bash/Zsh
source env/bin/activate

# Fish shell
source env/bin/activate.fish

# Csh/Tcsh
source env/bin/activate.csh
```

### **Deactivation:**
```bash
deactivate
```

### **Delete and Recreate Environment:**
```bash
# Remove old environment
rm -rf env

# Create new environment
python3 -m venv env

# Activate and install
source env/bin/activate
pip install -r requirements.txt
```

---

## 🎯 **Testing Your Setup**

### **Quick Test Commands:**
```bash
# Check Python version
python --version

# Check Django installation
python -c "import django; print(django.get_version())"

# Check if all apps can be imported
python manage.py check

# Test database connection
python manage.py dbshell

# List installed packages
pip list
```

### **Run the Verification Script:**
```bash
python verify_setup.py
```

---

## 🌐 **Network and Firewall Issues**

### **Allow Django port through firewall (Ubuntu):**
```bash
sudo ufw allow 8000
```

### **Check if service is running:**
```bash
netstat -tlnp | grep :8000
```

### **Access from other machines:**
```bash
# Run server on all interfaces
python manage.py runserver 0.0.0.0:8000

# Find your IP address
hostname -I
```

---

## 🔍 **Debugging Steps**

### **Enable Debug Mode:**
Make sure `DEBUG = True` in `mental_health_platform/settings.py`

### **Check Django Logs:**
```bash
# Run with verbose output
python manage.py runserver --verbosity=2

# Or check for specific errors
python manage.py check --deploy
```

### **Database Debugging:**
```bash
# Show migrations status
python manage.py showmigrations

# Reset migrations (DANGER!)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

---

## 📞 **Getting Help**

### **If you're still having issues:**

1. **Check the error logs** - Look for specific error messages
2. **Verify Python version** - Must be 3.8 or higher
3. **Check virtual environment** - Make sure it's activated
4. **Reinstall dependencies** - `pip install --force-reinstall -r requirements.txt`
5. **Try the Docker approach** - If all else fails

### **Common Error Patterns:**
- `ModuleNotFoundError` → Missing package, install with pip
- `Permission denied` → Don't use sudo with virtual environment
- `Port in use` → Use different port or kill existing process
- `Database locked` → Stop all Django processes and try again

---

**🎉 Your IndAid project should now work perfectly on Linux!**

For more help, check the main `INSTALLATION_GUIDE.md` or create an issue on the GitHub repository.
