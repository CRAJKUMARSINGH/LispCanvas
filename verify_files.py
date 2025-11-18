"""
Script to verify the content of the module files
"""

def verify_files():
    """Verify the content of the module files"""
    print("Verifying module files...")
    
    # Check rectangular_column.py
    try:
        with open('modules/rectangular_column.py', 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        print(f"Rectangular column file has {len(lines)} lines")
        
        # Check line 99 (0-indexed as 98)
        if len(lines) > 98:
            line_99 = lines[98]
            print(f"Line 99: {line_99}")
            
            if 'doc.write' in line_99:
                print("❌ Found doc.write in rectangular_column.py line 99")
                return False
            else:
                print("✅ No doc.write found in rectangular_column.py line 99")
        else:
            print(f"❌ File has only {len(lines)} lines")
            return False
            
    except Exception as e:
        print(f"Error reading rectangular_column.py: {e}")
        return False
    
    # Check circular_column_footing.py
    try:
        with open('modules/circular_column_footing.py', 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        print(f"Circular column footing file has {len(lines)} lines")
        
        # Check line 157 (0-indexed as 156)
        if len(lines) > 156:
            line_157 = lines[156]
            print(f"Line 157: {line_157}")
            
            if 'doc.write' in line_157:
                print("❌ Found doc.write in circular_column_footing.py line 157")
                return False
            else:
                print("✅ No doc.write found in circular_column_footing.py line 157")
        else:
            print(f"❌ File has only {len(lines)} lines")
            return False
            
    except Exception as e:
        print(f"Error reading circular_column_footing.py: {e}")
        return False
    
    print("✅ All files verified successfully")
    return True

if __name__ == "__main__":
    verify_files()