#!/usr/bin/env python3
"""
IndAid Mental Health Platform - Dependency Fix Script
This script fixes common dependency issues, especially the 'admin_interface' error.
"""

import sys
import subprocess
import os

def run_command(command, description):
    """Run a command and return success status"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def check_virtual_environment():
    """Check if virtual environment is activated"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        print("⚠️  WARNING: Virtual environment not detected!")
        print("For best results, activate your virtual environment first:")
        print("  Linux/macOS: source env/bin/activate")
        print("  Windows:     .\\venv\\Scripts\\Activate.ps1")
        print("")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    else:
        print("✅ Virtual environment detected")
    
    return True

def main():
    print("=" * 60)
    print("🔧 IndAid Dependency Fix Script")
    print("=" * 60)
    print("This script will fix common dependency issues.")
    print("")
    
    # Check virtual environment
    if not check_virtual_environment():
        return False
    
    # List of essential packages to install
    essential_packages = [
        "django==5.2.6",
        "django-admin-interface==0.30.1", 
        "django-colorfield==0.14.0",
        "pillow==11.3.0",
        "google-generativeai==0.8.5",
        "pydantic==2.11.9",
        "requests==2.32.5"
    ]
    
    print("\n🔧 FIXING DEPENDENCIES")
    print("=" * 40)
    
    # Step 1: Upgrade pip
    success = run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )
    
    # Step 2: Install essential packages individually
    for package in essential_packages:
        success = run_command(
            f"{sys.executable} -m pip install {package}",
            f"Installing {package.split('==')[0]}"
        )
        if not success:
            print(f"⚠️  Failed to install {package}, trying without version...")
            package_name = package.split('==')[0]
            run_command(
                f"{sys.executable} -m pip install {package_name}",
                f"Installing {package_name} (latest version)"
            )
    
    # Step 3: Install from requirements.txt if it exists
    if os.path.exists('requirements.txt'):
        print("\n📋 Installing from requirements.txt...")
        success = run_command(
            f"{sys.executable} -m pip install -r requirements.txt",
            "Installing all requirements"
        )
        
        if not success:
            print("⚠️  Some packages from requirements.txt failed to install")
            print("But essential packages should be working now.")
    
    # Step 4: Verify Django installation
    print("\n🔍 VERIFYING INSTALLATION")
    print("=" * 40)
    
    try:
        import django
        print(f"✅ Django {django.get_version()} installed successfully")
    except ImportError:
        print("❌ Django installation failed")
        return False
    
    try:
        import admin_interface
        print("✅ django-admin-interface installed successfully")
    except ImportError:
        print("❌ django-admin-interface still missing")
        print("Try running: pip install django-admin-interface")
        return False
    
    try:
        import colorfield
        print("✅ django-colorfield installed successfully")
    except ImportError:
        print("❌ django-colorfield still missing")
        print("Try running: pip install django-colorfield")
        return False
    
    # Step 5: Test Django project
    print("\n🚀 TESTING DJANGO PROJECT")
    print("=" * 40)
    
    if os.path.exists('manage.py'):
        success = run_command(
            f"{sys.executable} manage.py check",
            "Django project check"
        )
        
        if success:
            print("\n🎉 SUCCESS!")
            print("=" * 40)
            print("✅ All dependencies are now installed correctly!")
            print("✅ Django project passes all checks!")
            print("\n📝 You can now run:")
            print("   python manage.py runserver")
            print("\n🌐 Then visit:")
            print("   http://127.0.0.1:8000")
            return True
        else:
            print("\n⚠️  Django project check failed")
            print("But dependencies should be fixed now.")
            print("Try running: python manage.py runserver")
            return True
    else:
        print("⚠️  manage.py not found in current directory")
        print("Make sure you're in the project root directory")
        return False

if __name__ == "__main__":
    try:
        success = main()
        print("\n" + "=" * 60)
        if success:
            print("🏁 Dependency fix completed!")
        else:
            print("🔧 Some issues remain, check error messages above")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        print("Please try running the commands manually or check the documentation.")
