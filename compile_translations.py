#!/usr/bin/env python3
"""
Simple translation compiler to convert .po files to Django's .mo format
without requiring gettext tools.
"""
import os
import struct
from pathlib import Path

def parse_po_file(po_file_path):
    """Parse a .po file and extract msgid/msgstr pairs."""
    translations = {}
    current_msgid = ""
    current_msgstr = ""
    in_msgid = False
    in_msgstr = False
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
            
        if line.startswith('msgid '):
            if current_msgid and current_msgstr:
                translations[current_msgid] = current_msgstr
            current_msgid = line[7:-1]  # Remove 'msgid "' and '"'
            current_msgstr = ""
            in_msgid = True
            in_msgstr = False
            
        elif line.startswith('msgstr '):
            current_msgstr = line[8:-1]  # Remove 'msgstr "' and '"'
            in_msgid = False
            in_msgstr = True
            
        elif line.startswith('"') and line.endswith('"'):
            text = line[1:-1]  # Remove quotes
            if in_msgid:
                current_msgid += text
            elif in_msgstr:
                current_msgstr += text
    
    # Add the last translation pair
    if current_msgid and current_msgstr:
        translations[current_msgid] = current_msgstr
    
    # Remove empty msgid (header)
    if "" in translations:
        del translations[""]
    
    return translations

def write_mo_file(translations, mo_file_path):
    """Write translations to a .mo file in the format expected by Django."""
    import gettext
    
    # Use Python's built-in gettext module to create proper .mo files
    # First create a temporary dictionary with proper encoding
    catalog = {}
    
    for key, value in translations.items():
        # Ensure both key and value are properly encoded
        catalog[key.encode('utf-8')] = value.encode('utf-8')
    
    # Add empty key for metadata (required by gettext format)
    catalog[b''] = b'Content-Type: text/plain; charset=UTF-8\n'
    
    # Create a simple .mo file using the catalog
    keys = sorted(catalog.keys())
    values = [catalog[k] for k in keys]
    
    koffsets = []
    voffsets = []
    
    # Magic number for little-endian .mo files
    output = struct.pack('<I', 0x950412de)
    output += struct.pack('<I', 0)  # Version
    output += struct.pack('<I', len(keys))  # Number of strings
    
    # Offsets for key and value tables
    keystart = 7*4
    valuestart = keystart + 8*len(keys)
    
    output += struct.pack('<I', keystart)
    output += struct.pack('<I', valuestart)
    output += struct.pack('<I', 0)  # Hash table size (unused)
    output += struct.pack('<I', 0)  # Hash table offset (unused)
    
    # Calculate offsets
    offset = valuestart + 8*len(keys)
    
    for key in keys:
        koffsets.append((len(key), offset))
        offset += len(key) + 1  # +1 for null terminator
    
    for value in values:
        voffsets.append((len(value), offset))
        offset += len(value) + 1
    
    # Write key table
    for length, offset in koffsets:
        output += struct.pack('<I', length)
        output += struct.pack('<I', offset)
    
    # Write value table
    for length, offset in voffsets:
        output += struct.pack('<I', length)
        output += struct.pack('<I', offset)
    
    # Write strings
    for key in keys:
        output += key + b'\0'
    
    for value in values:
        output += value + b'\0'
    
    # Write the file
    with open(mo_file_path, 'wb') as f:
        f.write(output)

def compile_translations():
    """Find and compile all .po files in the locale directory."""
    base_dir = Path(__file__).parent
    locale_dir = base_dir / 'locale'
    
    if not locale_dir.exists():
        print("No locale directory found!")
        return
    
    compiled_count = 0
    
    for lang_dir in locale_dir.iterdir():
        if lang_dir.is_dir():
            po_file = lang_dir / 'LC_MESSAGES' / 'django.po'
            mo_file = lang_dir / 'LC_MESSAGES' / 'django.mo'
            
            if po_file.exists():
                print(f"Compiling {po_file}...")
                try:
                    translations = parse_po_file(po_file)
                    write_mo_file(translations, mo_file)
                    print(f"✓ Created {mo_file} with {len(translations)} translations")
                    compiled_count += 1
                except Exception as e:
                    print(f"✗ Error compiling {po_file}: {e}")
    
    print(f"\nCompiled {compiled_count} translation file(s).")

if __name__ == '__main__':
    compile_translations()
