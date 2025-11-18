#!/usr/bin/env python3
"""
Fix indentation issues in app.py
"""

def fix_indentation():
    with open('app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Fix the problematic lines
    for i, line in enumerate(lines):
        if i == 186:  # Line 187 (0-indexed)
            # Replace with correct indentation
            lines[i] = "    with col3:\n"
        elif i == 188:  # Line 189 (0-indexed)
            # Replace with correct indentation
            lines[i] = "    with col4:\n"
    
    # Write back to file
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Fixed indentation issues")

if __name__ == "__main__":
    fix_indentation()
