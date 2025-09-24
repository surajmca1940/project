#!/usr/bin/env python3
"""
IndAid Mental Health Platform - Setup Verification Script
This script verifies that the project is correctly installed and configured.
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version meets requirements"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_virtual_environment():
    """Check if virtual environment is activated"""
    print("\n🔧 Checking virtual environment...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
        return True
    else:
        print("⚠️  Virtual environment not detected (recommended but optional)")
        return True

def check_django():
    """Check Django installation and version"""
    print("\n🌐 Checking Django installation...")
    try:
        import django
        print(f"✅ Django {django.get_version()} - OK")
        return True
    except ImportError:
        print("❌ Django not found - run 'pip install -r requirements.txt'")
        return False

def check_required_packages():
    """Check if all required packages are installed"""
    print("\n📦 Checking required packages...")
    
    required_packages = [
        ('django', 'Django'),
        ('google.generativeai', 'Google Generative AI'),
        ('PIL', 'Pillow'),
        ('pydantic', 'Pydantic'),
        ('requests', 'Requests'),
    ]
    
    all_ok = True
    for package, name in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {name} - OK")
        except ImportError:
            print(f"❌ {name} - Missing")
            all_ok = False
    
    return all_ok

def check_project_structure():
    """Check if project files exist"""
    print("\n📁 Checking project structure...")
    
    required_files = [
        'manage.py',
        'requirements.txt',
        'mental_health_platform/settings.py',
        'accounts',
        'ai_support',
        'booking_system',
        'static',
        'templates'
    ]
    
    all_ok = True
    for item in required_files:
        if os.path.exists(item):
            print(f"✅ {item} - Found")
        else:
            print(f"❌ {item} - Missing")
            all_ok = False
    
    return all_ok

def check_database():
    """Check if database is set up"""
    print("\n🗄️  Checking database...")
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health_platform.settings')
        
        import django
        django.setup()
        
        from django.core.management import execute_from_command_line
        from django.db import connection
        
        # Try to connect to database
        connection.ensure_connection()
        print("✅ Database connection - OK")
        
        # Check if migrations are applied
        result = subprocess.run([sys.executable, 'manage.py', 'showmigrations'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            if '[X]' in output:
                print("✅ Database migrations - Applied")
                return True
            else:
                print("⚠️  Database migrations - Need to run 'python manage.py migrate'")
                return True
        else:
            print("❌ Database migrations check failed")
            return False
            
    except Exception as e:
        print(f"❌ Database issue: {str(e)}")
        return False

def check_static_files():
    """Check if static files are set up"""
    print("\n🎨 Checking static files...")
    
    static_dirs = ['static/css', 'static/js']
    all_ok = True
    
    for dir_path in static_dirs:
        if os.path.exists(dir_path) and os.listdir(dir_path):
            print(f"✅ {dir_path} - Found with files")
        else:
            print(f"⚠️  {dir_path} - Empty or missing")
            all_ok = False
    
    return all_ok

def test_django_server():
    """Test if Django server can start"""
    print("\n🚀 Testing Django server startup...")
    try:
        result = subprocess.run([sys.executable, 'manage.py', 'check'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Django project check - Passed")
            print("✅ Server should start successfully")
            return True
        else:
            print("❌ Django project check - Failed")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️  Django check timed out")
        return False
    except Exception as e:
        print(f"❌ Django check failed: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("=" * 60)
    print("🏥 IndAid Mental Health Platform - Setup Verification")
    print("=" * 60)
    
    checks = [
        check_python_version,
        check_virtual_environment, 
        check_django,
        check_required_packages,
        check_project_structure,
        check_database,
        check_static_files,
        test_django_server
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Check failed with error: {str(e)}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL CHECKS PASSED ({passed}/{total})")
        print("\n✅ Your IndAid project is ready to run!")
        print("📝 To start the server: python manage.py runserver")
        print("🌐 Then visit: http://127.0.0.1:8000")
        
    elif passed >= total - 2:
        print(f"⚠️  MOSTLY READY ({passed}/{total})")
        print("🔧 Minor issues detected but project should still work")
        print("📝 Try running: python manage.py runserver")
        
    else:
        print(f"❌ ISSUES FOUND ({passed}/{total})")
        print("🔧 Please fix the issues above before running the project")
        print("📚 Check INSTALLATION_GUIDE.md for help")
    
    print("\n📋 Quick Commands:")
    print("• python manage.py runserver       - Start server")
    print("• python manage.py migrate         - Apply database migrations")
    print("• python manage.py createsuperuser - Create admin user")
    print("• python manage.py collectstatic   - Collect static files")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Verification script error: {str(e)}")
        sys.exit(1)
