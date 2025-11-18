#!/usr/bin/env python3
"""
Simple syntax test for app.py
"""

def test_syntax():
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for problematic characters
        lines = content.split('\n')
        for i, line in enumerate(lines[180:200], 181):
            print(f"Line {i}: {repr(line)}")
            
        # Try to compile
        compile(content, 'app.py', 'exec')
        print("✅ Syntax is correct")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error at line {e.lineno}: {e.msg}")
        print(f"Text: {repr(e.text)}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_syntax()
