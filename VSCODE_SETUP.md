# VS Code Setup Guide for IndAid Project

## 🚀 Quick Start

### 1. First Time Setup
Once VS Code opens, you'll see a notification to install recommended extensions. Click **"Install All"**.

### 2. Python Interpreter
1. Press `Ctrl+Shift+P` to open Command Palette
2. Type "Python: Select Interpreter" 
3. Choose `./venv/Scripts/python.exe` (should be auto-detected)

### 3. Running the Project

#### Method 1: Using Tasks (Recommended)
- Press `Ctrl+Shift+P` → Type "Tasks: Run Task"
- Select "Django: Run Server" 
- Server will start at `http://127.0.0.1:8000`

#### Method 2: Using Debug Mode
- Press `F5` or go to Run & Debug panel (`Ctrl+Shift+D`)
- Select "Django: Debug Server"
- Click the green play button

#### Method 3: Using Terminal
- Press `Ctrl+`` (backtick) to open terminal
- Type: `python manage.py runserver`

### 4. Essential Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+P` | Command Palette |
| `Ctrl+`` | Toggle Terminal |
| `F5` | Start Debugging |
| `Ctrl+Shift+D` | Debug Panel |
| `Ctrl+Shift+E` | Explorer Panel |
| `Ctrl+Shift+G` | Git Panel |
| `Ctrl+B` | Toggle Sidebar |

## 🛠️ Essential Extensions (Auto-installed)

### Django Development
- **Django** - Template syntax highlighting
- **Python** - Python language support
- **Pylance** - Advanced Python IntelliSense

### Web Development  
- **HTML CSS Support** - Better HTML/CSS editing
- **Auto Rename Tag** - Automatic HTML tag renaming

### Database
- **SQLite Viewer** - View your SQLite database

### Git Integration
- **GitLens** - Enhanced Git capabilities
- **Git Graph** - Visual git history

## 🔧 Key Features Enabled

### 1. Intelligent Code Completion
- Auto-complete for Django models, views, templates
- Import suggestions
- Function parameter hints

### 2. Debugging
- Set breakpoints in Python code
- Step through Django views
- Inspect variables and database queries

### 3. Django Template Support
- Syntax highlighting for `.html` files
- Django template tags and filters
- Emmet support in templates

### 4. Database Integration
- View SQLite database content
- Run SQL queries directly in VS Code

### 5. Git Integration
- Visual diff viewer
- Commit history
- Branch management

## 🏃‍♂️ Running Different Django Commands

### Using Tasks (Ctrl+Shift+P → "Tasks: Run Task")
- **Django: Run Server** - Start development server
- **Django: Make Migrations** - Create new migrations
- **Django: Migrate** - Apply migrations
- **Django: Collect Static** - Collect static files
- **Django: Create Superuser** - Create admin user
- **Django: Test** - Run tests

### Using Terminal
```bash
# Development server
python manage.py runserver

# Database operations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

## 🎯 Pro Tips

### 1. Quick File Navigation
- `Ctrl+P` - Quick open files
- `Ctrl+T` - Go to symbol in workspace
- `Ctrl+G` - Go to line number

### 2. Django-Specific Tips
- Use `Ctrl+Click` on model names to jump to definition
- Hover over Django functions for documentation
- Use auto-import for Django imports

### 3. Debugging Tips
- Set breakpoints by clicking left of line numbers
- Use `print()` statements for quick debugging
- Check Django Debug Toolbar in browser

### 4. Terminal Management
- `Ctrl+Shift+`` - New terminal
- Multiple terminals for different tasks
- Terminal automatically activates virtual environment

## 🔍 Troubleshooting

### Python Interpreter Issues
```bash
# If VS Code doesn't detect interpreter
Ctrl+Shift+P → "Python: Select Interpreter" → Choose ./venv/Scripts/python.exe
```

### Django Not Found
```bash
# Make sure virtual environment is activated
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
# Or use the pre-configured task "Django: Run Server (Port 8001)"
```

### Extensions Not Working
1. Restart VS Code
2. Check if extensions are enabled
3. Reload Window: `Ctrl+Shift+P` → "Developer: Reload Window"

## 📚 Useful Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [Django in VS Code](https://code.visualstudio.com/docs/python/tutorial-django)

---

**Happy Coding! 🎉**
Your IndAid Mental Health Platform is now ready for development in VS Code!
