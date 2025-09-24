# IndAid - Complete Installation Guide

## 🚀 **System Requirements**

### **Operating System**
- ✅ **Windows 10/11** (64-bit) - Primary support
- ✅ **macOS 10.15+** - Compatible
- ✅ **Linux Ubuntu 18.04+** - Compatible

### **Hardware Requirements**
- **RAM:** Minimum 4GB, Recommended 8GB+
- **Storage:** At least 2GB free space
- **CPU:** Any modern processor (x64)

---

## 📋 **Prerequisites Installation Checklist**

### **1. Python 3.8+ Installation**

#### **Windows:**
```powershell
# Method 1: Download from official website
https://www.python.org/downloads/

# Method 2: Using winget (Windows 11/10 with App Installer)
winget install Python.Python.3.12

# Method 3: Using Chocolatey (if installed)
choco install python3
```

#### **Verification:**
```bash
python --version
# Should show: Python 3.8.x or higher (tested with 3.12.10)

pip --version  
# Should show pip version
```

### **2. Git Version Control**

#### **Windows:**
```powershell
# Method 1: Download from official website
https://git-scm.com/download/win

# Method 2: Using winget
winget install Git.Git

# Method 3: Using Chocolatey
choco install git
```

#### **Verification:**
```bash
git --version
# Should show: git version 2.40+
```

### **3. VS Code (Recommended IDE)**

#### **Windows:**
```powershell
# Method 1: Download from official website
https://code.visualstudio.com/

# Method 2: Using winget
winget install Microsoft.VisualStudioCode

# Method 3: Using Chocolatey
choco install vscode
```

### **4. Node.js (For Frontend Tooling)**

#### **Windows:**
```powershell
# Download from official website
https://nodejs.org/

# Or using winget
winget install OpenJS.NodeJS

# Or using Chocolatey
choco install nodejs
```

#### **Verification:**
```bash
node --version
# Should show: v16.0.0 or higher

npm --version
# Should show: npm version
```

---

## 🛠️ **Project Setup Instructions**

### **Step 1: Clone the Repository**
```bash
# Clone the project
git clone <your-repository-url>
cd digital-psychological-intervention-system

# Or if you have the project folder
cd path/to/your/project
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows Command Prompt:
venv\Scripts\activate.bat

# macOS/Linux:
source venv/bin/activate
```

### **Step 3: Install Python Dependencies**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### **Step 4: Database Setup**
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### **Step 5: Static Files Setup**
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### **Step 6: Run the Development Server**
```bash
# Start the server
python manage.py runserver

# Or on a different port
python manage.py runserver 8001
```

---

## 📦 **Complete Dependencies List**

### **Python Dependencies (requirements.txt)**
```txt
annotated-types==0.7.0
asgiref==3.9.1
cachetools==5.5.2
certifi==2025.8.3
charset-normalizer==3.4.3
Django==5.2.6
django-admin-interface==0.30.1
django-colorfield==0.14.0
google-ai-generativelanguage==0.6.15
google-api-core==2.25.1
google-api-python-client==2.182.0
google-auth==2.40.3
google-auth-httplib2==0.2.0
google-generativeai==0.8.5
googleapis-common-protos==1.70.0
grpcio==1.75.0
grpcio-status==1.71.2
httplib2==0.31.0
idna==3.10
pillow==11.3.0
proto-plus==1.26.1
protobuf==5.29.5
pyasn1==0.6.1
pyasn1_modules==0.4.2
pydantic==2.11.9
pydantic_core==2.33.2
pyparsing==3.2.5
python-slugify==8.0.4
requests==2.32.5
rsa==4.9.1
sqlparse==0.5.3
text-unidecode==1.3
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.15.0
tzdata==2025.2
uritemplate==4.2.0
urllib3==2.5.0
```

### **Development Dependencies (Optional)**
```bash
# Code formatting and linting
pip install black flake8 autopep8

# Testing
pip install pytest pytest-django

# Documentation
pip install sphinx

# Database tools
pip install django-extensions
```

### **Node.js Dependencies (package.json)**
```json
{
  "devDependencies": {
    "concurrently": "^8.2.2"
  },
  "engines": {
    "node": ">=16.0.0",
    "npm": ">=8.0.0"
  }
}
```

---

## 🔧 **VS Code Extensions List**

### **Essential Extensions (Auto-install)**
Copy this into `.vscode/extensions.json`:
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.pylint",
    "ms-python.black-formatter",
    "batisteo.vscode-django",
    "thebarkman.vscode-djaneiro",
    "bibhasdn.django-html",
    "ecmel.vscode-html-css",
    "formulahendry.auto-close-tag",
    "alexcvzz.vscode-sqlite",
    "eamodio.gitlens",
    "ms-vscode.powershell",
    "yzhang.markdown-all-in-one",
    "ms-python.vscode-pylance",
    "ritwickdey.liveserver",
    "VisualStudioExptTeam.vscodeintellicode"
  ]
}
```

---

## 🌐 **Environment Variables**

### **Required Environment Variables**
Create a `.env` file in project root:
```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Google Gemini AI (Optional - for AI features)
GEMINI_API_KEY=your-gemini-api-key-here

# Database (for production)
DATABASE_URL=your-database-url-here

# Time Zone
TIME_ZONE=Asia/Kolkata
```

---

## 📁 **Project Structure Overview**
```
digital-psychological-intervention-system/
├── accounts/                 # User authentication
├── admin_dashboard/          # Admin analytics
├── ai_support/              # AI chatbot functionality
├── booking_system/          # Appointment booking
├── mental_health_platform/  # Core Django app
├── peer_support/            # Community forums
├── resources/               # Educational content
├── static/                  # CSS, JS, images
├── templates/               # HTML templates
├── venv/                    # Virtual environment
├── .vscode/                 # VS Code configuration
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies
└── README.md              # Project documentation
```

---

## 🚀 **Quick Setup Script (Windows)**

Create `setup.bat` for automated setup:
```batch
@echo off
echo Setting up IndAid Mental Health Platform...

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install -r requirements.txt

echo Setting up database...
python manage.py makemigrations
python manage.py migrate

echo Collecting static files...
python manage.py collectstatic --noinput

echo Setup complete! Run 'python manage.py runserver' to start the server.
pause
```

### **PowerShell Setup Script**
Create `setup.ps1`:
```powershell
Write-Host "Setting up IndAid Mental Health Platform..." -ForegroundColor Green

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Database setup
Write-Host "Setting up database..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Run 'python manage.py runserver' to start the server." -ForegroundColor Cyan
```

---

## 🔍 **Troubleshooting Common Issues**

### **1. Python Not Found**
```bash
# Add Python to PATH or reinstall Python with "Add to PATH" option checked
# Verify installation:
where python
# Should show Python installation path
```

### **2. pip Not Working**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Or reinstall pip
python -m ensurepip --upgrade
```

### **3. Virtual Environment Issues**
```bash
# Delete and recreate virtual environment
rm -rf venv  # or rmdir /s venv on Windows
python -m venv venv
```

### **4. Permission Errors (Windows)**
```powershell
# Run PowerShell as Administrator or change execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **5. Port Already in Use**
```bash
# Use different port
python manage.py runserver 8001

# Or find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### **6. Missing Dependencies**
```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt
```

---

## 📋 **Pre-deployment Checklist**

### **Development Setup ✅**
- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] VS Code installed (optional)
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database migrated
- [ ] Static files collected
- [ ] Server running successfully

### **Production Setup (Future)**
- [ ] PostgreSQL/MySQL database
- [ ] Web server (Nginx/Apache)
- [ ] WSGI server (Gunicorn/uWSGI)
- [ ] SSL certificate
- [ ] Environment variables configured
- [ ] Static files served properly
- [ ] Domain configured

---

## 🎯 **Verification Commands**

Run these commands to verify your setup:
```bash
# Check Python version
python --version

# Check Django installation
python -c "import django; print(django.get_version())"

# Check all dependencies
pip list

# Test Django project
python manage.py check

# Run tests (if available)
python manage.py test
```

---

## 📞 **Support & Resources**

### **Documentation Links**
- [Django Documentation](https://docs.djangoproject.com/)
- [Python Documentation](https://docs.python.org/3/)
- [Git Documentation](https://git-scm.com/doc)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)

### **Community Support**
- Django Community: https://www.djangoproject.com/community/
- Stack Overflow: https://stackoverflow.com/questions/tagged/django
- Python Community: https://www.python.org/community/

---

**🎉 Congratulations!** 
Your IndAid Mental Health Platform development environment is now ready!
