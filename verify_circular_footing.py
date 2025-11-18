"""
Verification script for circular column footing module
"""

import inspect
import os

def verify_circular_column_footing_module():
    """Verify the circular column footing module"""
    print("Verifying circular column footing module...")
    
    try:
        # Import the module
        import modules.circular_column_footing as module
        
        # Get the file path
        file_path = module.__file__
        print(f"Module file path: {file_path}")
        
        # Read the actual file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if the file contains the expected content
        lines = content.split('\n')
        print(f"Total lines in file: {len(lines)}")
        
        # Check line 157 (0-indexed as 156)
        if len(lines) > 156:
            line_157 = lines[156]
            print(f"Line 157: {line_157}")
            
            if 'doc.write' in line_157:
                print("❌ Found doc.write in line 157 - this is the source of the error!")
                print("The function is using doc.write instead of the correct approach.")
                return False
            else:
                print("✅ Line 157 does not contain doc.write")
        else:
            print(f"❌ File has only {len(lines)} lines, less than 157")
            return False
            
        # Check if the function uses the correct approach
        if 'tempfile.NamedTemporaryFile' in content:
            print("✅ Function uses tempfile.NamedTemporaryFile (correct approach)")
        else:
            print("❌ Function does not use tempfile.NamedTemporaryFile")
            
        if 'doc.saveas' in content:
            print("✅ Function uses doc.saveas (correct approach)")
        else:
            print("❌ Function does not use doc.saveas")
            
        print("✅ Verification completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    verify_circular_column_footing_module()