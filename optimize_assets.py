#!/usr/bin/env python3
"""
Asset Optimization Script for Mental Health Booking System
Minifies CSS and JavaScript files for better performance.
"""

import os
import re
import gzip
import json
from pathlib import Path

def minify_css(css_content):
    """Minify CSS content by removing unnecessary whitespace and comments."""
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # Remove unnecessary whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    css_content = re.sub(r';\s*}', '}', css_content)
    css_content = re.sub(r'{\s*', '{', css_content)
    css_content = re.sub(r'}\s*', '}', css_content)
    css_content = re.sub(r':\s*', ':', css_content)
    css_content = re.sub(r';\s*', ';', css_content)
    css_content = re.sub(r',\s*', ',', css_content)
    
    # Remove leading/trailing whitespace
    css_content = css_content.strip()
    
    return css_content

def minify_js(js_content):
    """Basic JavaScript minification."""
    # Remove single-line comments (but preserve URLs and regex)
    js_content = re.sub(r'(?<!:)//(?![^\r\n]*["\']).*', '', js_content)
    
    # Remove multi-line comments
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    
    # Remove unnecessary whitespace
    js_content = re.sub(r'\s+', ' ', js_content)
    js_content = re.sub(r'\s*([{}();,:])\s*', r'\1', js_content)
    
    # Remove trailing semicolons before }
    js_content = re.sub(r';\s*}', '}', js_content)
    
    return js_content.strip()

def gzip_file(content, filename):
    """Create gzipped version of the file."""
    gzip_filename = filename + '.gz'
    with gzip.open(gzip_filename, 'wt', encoding='utf-8') as f:
        f.write(content)
    return gzip_filename

def optimize_file(file_path):
    """Optimize a single file."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"⚠️  File not found: {file_path}")
        return
    
    print(f"📄 Processing {file_path.name}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    original_size = len(original_content)
    
    if file_path.suffix == '.css':
        minified_content = minify_css(original_content)
    elif file_path.suffix == '.js':
        minified_content = minify_js(original_content)
    else:
        print(f"⚠️  Unsupported file type: {file_path.suffix}")
        return
    
    minified_size = len(minified_content)
    
    # Create minified version
    minified_path = file_path.parent / f"{file_path.stem}.min{file_path.suffix}"
    with open(minified_path, 'w', encoding='utf-8') as f:
        f.write(minified_content)
    
    # Create gzipped version
    gzip_path = gzip_file(minified_content, str(minified_path))
    gzip_size = os.path.getsize(gzip_path)
    
    # Calculate savings
    size_reduction = ((original_size - minified_size) / original_size) * 100
    gzip_reduction = ((original_size - gzip_size) / original_size) * 100
    
    print(f"✅ {file_path.name}")
    print(f"   Original: {original_size:,} bytes")
    print(f"   Minified: {minified_size:,} bytes ({size_reduction:.1f}% reduction)")
    print(f"   Gzipped:  {gzip_size:,} bytes ({gzip_reduction:.1f}% reduction)")
    print()

def create_asset_manifest():
    """Create manifest of optimized assets."""
    manifest = {
        "version": "1.0",
        "generated": "2024-01-01",
        "files": {}
    }
    
    static_dir = Path("static")
    
    for css_file in static_dir.rglob("*.min.css"):
        original_file = css_file.parent / f"{css_file.stem.replace('.min', '')}.css"
        if original_file.exists():
            manifest["files"][str(original_file)] = str(css_file)
    
    for js_file in static_dir.rglob("*.min.js"):
        original_file = js_file.parent / f"{js_file.stem.replace('.min', '')}.js"
        if original_file.exists():
            manifest["files"][str(original_file)] = str(js_file)
    
    with open("static/asset-manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print("📋 Created asset manifest: static/asset-manifest.json")

def main():
    """Main optimization function."""
    print("🚀 Starting asset optimization...\n")
    
    # Files to optimize
    files_to_optimize = [
        "static/css/booking-smooth.css",
        "static/js/booking-optimized.js",
        "static/js/booking-sw.js",
        "static/css/style.css",
        "static/js/main.js"
    ]
    
    total_original = 0
    total_minified = 0
    total_gzipped = 0
    
    for file_path in files_to_optimize:
        if Path(file_path).exists():
            optimize_file(file_path)
            
            # Calculate totals
            original_size = os.path.getsize(file_path)
            minified_path = Path(file_path).parent / f"{Path(file_path).stem}.min{Path(file_path).suffix}"
            gzipped_path = str(minified_path) + '.gz'
            
            if minified_path.exists():
                minified_size = os.path.getsize(minified_path)
                total_original += original_size
                total_minified += minified_size
                
                if os.path.exists(gzipped_path):
                    gzipped_size = os.path.getsize(gzipped_path)
                    total_gzipped += gzipped_size
    
    # Create asset manifest
    create_asset_manifest()
    
    # Summary
    if total_original > 0:
        minified_reduction = ((total_original - total_minified) / total_original) * 100
        gzipped_reduction = ((total_original - total_gzipped) / total_original) * 100
        
        print("=" * 50)
        print("📊 OPTIMIZATION SUMMARY")
        print("=" * 50)
        print(f"Total Original Size: {total_original:,} bytes")
        print(f"Total Minified Size: {total_minified:,} bytes ({minified_reduction:.1f}% reduction)")
        print(f"Total Gzipped Size:  {total_gzipped:,} bytes ({gzipped_reduction:.1f}% reduction)")
        print()
        print("💡 Don't forget to:")
        print("   1. Update your templates to use .min.css and .min.js files")
        print("   2. Configure your web server to serve pre-compressed .gz files")
        print("   3. Set appropriate cache headers for static assets")
        print("   4. Enable Brotli compression if possible")
        print()
        print("🎉 Optimization complete!")

if __name__ == "__main__":
    main()