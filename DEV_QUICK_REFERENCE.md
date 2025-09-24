# 🚀 IndAid - Developer Quick Reference

## 📋 **Installation Checklist**

### **Prerequisites** ✅
- [ ] **Python 3.8+** - `python --version`
- [ ] **Git** - `git --version`  
- [ ] **VS Code** (recommended) - [Download](https://code.visualstudio.com/)
- [ ] **Node.js** (optional) - `node --version`

### **Project Setup** ✅
- [ ] **Clone/Download** project files
- [ ] **Virtual Environment** - `python -m venv venv`
- [ ] **Activate venv** - `.\venv\Scripts\Activate.ps1` (PowerShell) or `venv\Scripts\activate.bat` (CMD)
- [ ] **Install Dependencies** - `pip install -r requirements.txt`
- [ ] **Database Setup** - `python manage.py migrate`
- [ ] **Static Files** - `python manage.py collectstatic --noinput`

---

## ⚡ **Quick Start Commands**

### **One-Line Setup (Windows)**
```batch
# Batch script - Double click setup.bat
setup.bat

# Or PowerShell script
.\setup.ps1
```

### **Manual Setup**
```bash
# 1. Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # PowerShell
# OR
venv\Scripts\activate.bat    # Command Prompt

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python manage.py migrate

# 4. Run server
python manage.py runserver
```

---

## 🛠️ **Essential Django Commands**

### **Development Server**
```bash
# Start server (default port 8000)
python manage.py runserver

# Start on different port
python manage.py runserver 8001

# Start with specific IP (for network access)
python manage.py runserver 0.0.0.0:8000
```

### **Database Operations**
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migrations status
python manage.py showmigrations

# Reset database (DANGER!)
python manage.py flush
```

### **User Management**
```bash
# Create admin user
python manage.py createsuperuser

# Change user password
python manage.py changepassword <username>
```

### **Static Files**
```bash
# Collect static files
python manage.py collectstatic

# Collect without confirmation
python manage.py collectstatic --noinput

# Clear collected files
python manage.py collectstatic --clear
```

### **Django Shell & Testing**
```bash
# Open Django shell
python manage.py shell

# Run tests
python manage.py test

# Check for issues
python manage.py check

# Show Django version
python -c "import django; print(django.get_version())"
```

---

## 💻 **VS Code Setup**

### **Open Project**
```bash
# Open current directory in VS Code
code .

# Open specific folder
code C:\path\to\your\project
```

### **Essential Extensions (Auto-installed)**
- **Python** - Python language support
- **Django** - Django template support  
- **Pylance** - Advanced Python IntelliSense
- **GitLens** - Enhanced Git integration
- **SQLite Viewer** - Database viewer

### **VS Code Shortcuts**
| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+P` | Command Palette |
| `Ctrl+`` | Toggle Terminal |
| `F5` | Start Debugging |
| `Ctrl+P` | Quick File Open |
| `Ctrl+Shift+G` | Git Panel |

---

## 🌐 **Access URLs**

### **Development URLs**
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **AI Support**: http://127.0.0.1:8000/ai-support/
- **Booking**: http://127.0.0.1:8000/booking/
- **Resources**: http://127.0.0.1:8000/resources/
- **Community**: http://127.0.0.1:8000/community/
- **Dashboard**: http://127.0.0.1:8000/dashboard/

### **Alternative Port URLs** (if using port 8001)
- **Main App**: http://127.0.0.1:8001/
- **Admin Panel**: http://127.0.0.1:8001/admin/

---

## 📦 **Python Dependencies Overview**

### **Core Framework**
- **Django 5.2.6** - Web framework
- **Python 3.12.10** - Programming language

### **AI & Machine Learning**
- **google-generativeai** - Google Gemini AI
- **pydantic** - Data validation

### **Image & Media**
- **Pillow** - Image processing

### **Database**
- **SQLite** (development)
- **PostgreSQL ready** (production)

---

## 🔧 **Troubleshooting Quick Fixes**

### **Common Issues**
```bash
# Python not found
where python  # Check if Python in PATH

# Permission denied (PowerShell)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Port already in use
python manage.py runserver 8001  # Use different port

# Virtual environment issues
rmdir /s venv  # Delete and recreate
python -m venv venv

# Dependencies issues
pip install --force-reinstall -r requirements.txt

# Database locked
# Close all connections and restart server

# Static files not loading
python manage.py collectstatic --noinput
# Hard refresh browser: Ctrl+F5
```

### **Reset Everything**
```bash
# Nuclear option - reset everything
rmdir /s venv
rmdir /s staticfiles  
del db.sqlite3
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## 📂 **Project Structure**

```
IndAid-Project/
├── 📁 accounts/          # User authentication
├── 📁 admin_dashboard/   # Analytics dashboard  
├── 📁 ai_support/        # AI chatbot
├── 📁 booking_system/    # Appointment booking
├── 📁 mental_health_platform/  # Core app
├── 📁 peer_support/      # Community forums
├── 📁 resources/         # Educational content
├── 📁 static/           # CSS, JS, images
├── 📁 templates/        # HTML templates
├── 📁 venv/            # Virtual environment
├── 📁 .vscode/         # VS Code config
├── 📄 manage.py        # Django management
├── 📄 requirements.txt # Python packages
├── 📄 db.sqlite3      # Database file
├── 📄 setup.bat       # Windows setup script
└── 📄 setup.ps1       # PowerShell setup script
```

---

## 🎯 **Development Workflow**

### **Daily Development**
1. **Activate venv**: `.\venv\Scripts\Activate.ps1`
2. **Pull updates**: `git pull`
3. **Check migrations**: `python manage.py showmigrations`
4. **Apply if needed**: `python manage.py migrate`
5. **Start server**: `python manage.py runserver`
6. **Open VS Code**: `code .`

### **After Making Changes**
1. **Create migrations**: `python manage.py makemigrations`
2. **Apply migrations**: `python manage.py migrate`
3. **Test changes**: Browse to localhost:8000
4. **Commit changes**: `git add . && git commit -m "Description"`

---

## 📱 **Testing URLs**

### **Feature Testing**
- **Home Page**: http://127.0.0.1:8000/
- **Login/Register**: http://127.0.0.1:8000/login/
- **AI Chat**: http://127.0.0.1:8000/ai-support/
- **Book Appointment**: http://127.0.0.1:8000/booking/
- **Resources**: http://127.0.0.1:8000/resources/
- **Peer Support**: http://127.0.0.1:8000/community/
- **Admin Dashboard**: http://127.0.0.1:8000/admin/

---

**🎉 Happy Coding!**
*Keep this reference handy for quick development tasks!*
