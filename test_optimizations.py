#!/usr/bin/env python3
"""
Test script to verify booking system optimizations
"""

import os
import time
from pathlib import Path

def test_file_exists(file_path, description):
    """Test if a file exists."""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def test_file_size(original_path, minified_path, description):
    """Test if minified file is smaller than original."""
    if os.path.exists(original_path) and os.path.exists(minified_path):
        original_size = os.path.getsize(original_path)
        minified_size = os.path.getsize(minified_path)
        reduction = ((original_size - minified_size) / original_size) * 100
        
        if minified_size < original_size:
            print(f"✅ {description}: {reduction:.1f}% smaller")
            return True
        else:
            print(f"❌ {description}: Minified file is larger!")
            return False
    else:
        print(f"⚠️  {description}: Files not found for comparison")
        return False

def main():
    """Main test function."""
    print("🧪 Testing Booking System Optimizations\n")
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Check if optimized files exist
    test_files = [
        ("static/css/booking-smooth.css", "Enhanced CSS file"),
        ("static/js/booking-optimized.js", "Optimized JavaScript file"),
        ("static/js/booking-sw.js", "Service Worker file"),
        ("optimize_assets.py", "Asset optimization script"),
        ("PERFORMANCE_GUIDE.md", "Performance guide documentation")
    ]
    
    print("📋 File Existence Tests:")
    for file_path, description in test_files:
        if test_file_exists(file_path, description):
            tests_passed += 1
        total_tests += 1
    
    print("\n📦 Minification Tests:")
    minification_tests = [
        ("static/css/booking-smooth.css", "static/css/booking-smooth.min.css", "CSS minification"),
        ("static/js/booking-optimized.js", "static/js/booking-optimized.min.js", "JS minification"),
        ("static/js/booking-sw.js", "static/js/booking-sw.min.js", "Service Worker minification"),
        ("static/css/style.css", "static/css/style.min.css", "Main CSS minification"),
        ("static/js/main.js", "static/js/main.min.js", "Main JS minification")
    ]
    
    for original, minified, description in minification_tests:
        if test_file_size(original, minified, description):
            tests_passed += 1
        total_tests += 1
    
    print("\n🗜️  Compression Tests:")
    gzip_tests = [
        ("static/css/booking-smooth.min.css.gz", "CSS Gzip compression"),
        ("static/js/booking-optimized.min.js.gz", "JS Gzip compression"),
        ("static/js/booking-sw.min.js.gz", "Service Worker Gzip compression")
    ]
    
    for gzip_file, description in gzip_tests:
        if test_file_exists(gzip_file, description):
            tests_passed += 1
        total_tests += 1
    
    print("\n🔍 Feature Tests:")
    
    # Test template updates
    template_path = "templates/booking_system/appointments_enhanced.html"
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        features_to_check = [
            ("booking-optimized.js", "Optimized JavaScript inclusion"),
            ("booking-smooth.css", "Enhanced CSS inclusion"),
            ("lazy-image", "Lazy loading implementation"),
            ("aria-label", "Accessibility enhancements"),
            ("data-haptic", "Mobile haptic feedback")
        ]
        
        for feature, description in features_to_check:
            if feature in template_content:
                print(f"✅ {description}")
                tests_passed += 1
            else:
                print(f"❌ {description}: Not found in template")
            total_tests += 1
    else:
        print("❌ Template file not found")
        total_tests += 5  # All feature tests failed
    
    # Test asset manifest
    print("\n📄 Asset Manifest Test:")
    if test_file_exists("static/asset-manifest.json", "Asset manifest"):
        tests_passed += 1
    total_tests += 1
    
    # Final results
    print("\n" + "="*50)
    print(f"🎯 Test Results: {tests_passed}/{total_tests} tests passed")
    print("="*50)
    
    success_rate = (tests_passed / total_tests) * 100
    
    if success_rate >= 90:
        print("🎉 EXCELLENT! Your booking system is optimized and ready!")
        print("\n🚀 Next steps:")
        print("   1. Test the booking flow in your browser")
        print("   2. Run: python manage.py runserver")
        print("   3. Visit: http://localhost:8000/booking/appointments/")
        print("   4. Check mobile responsiveness")
        print("   5. Test performance with browser dev tools")
    elif success_rate >= 75:
        print("✨ GOOD! Most optimizations are in place.")
        print("   Review the failed tests and address any issues.")
    else:
        print("⚠️  Some optimizations are missing.")
        print("   Please run the optimization script and check the failed tests.")
    
    # Performance tips
    print("\n💡 Performance Tips:")
    print("   • Use 'python optimize_assets.py' to update minified files")
    print("   • Test on mobile devices for touch interactions")
    print("   • Monitor Core Web Vitals in production")
    print("   • Enable gzip compression on your web server")
    
    return success_rate >= 75

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)