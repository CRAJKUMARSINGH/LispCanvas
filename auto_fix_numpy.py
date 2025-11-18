"""
Automatic NumPy fixer for LispCanvas
This script automatically fixes the NumPy compatibility issue
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def fix_numpy_issue():
    """Automatically fix the NumPy issue"""
    print("=" * 50)
    print("AUTOMATIC NUMPY FIXER FOR LISPCANVAS")
    print("=" * 50)
    
    print("\n1. Checking current NumPy version...")
    try:
        import numpy as np
        print(f"   Current NumPy version: {getattr(np, '__version__', 'unknown')}")
    except ImportError:
        print("   NumPy is not installed")
    except Exception as e:
        print(f"   Error importing NumPy: {e}")
    
    print("\n2. Uninstalling current NumPy...")
    success, stdout, stderr = run_command("pip uninstall numpy -y")
    if success:
        print("   Successfully uninstalled NumPy")
    else:
        print(f"   Error uninstalling NumPy: {stderr}")
        return False
    
    print("\n3. Installing compatible NumPy version (1.24.3)...")
    success, stdout, stderr = run_command("pip install numpy==1.24.3")
    if success:
        print("   Successfully installed NumPy 1.24.3")
    else:
        print(f"   Error installing NumPy: {stderr}")
        return False
    
    print("\n4. Verifying the fix...")
    try:
        # Restart Python to clear any cached imports
        import importlib
        import sys
        
        # Clear numpy from sys.modules if it exists
        modules_to_remove = [key for key in sys.modules.keys() if key.startswith('numpy')]
        for module in modules_to_remove:
            del sys.modules[module]
        
        # Import numpy again
        import numpy as np
        result = getattr(np, 'pi', 3.14159) * 2
        print(f"   Success! NumPy is working correctly.")
        print(f"   NumPy version: {getattr(np, '__version__', 'unknown')}")
        print(f"   Test calculation (π * 2): {result:.6f}")
        return True
    except Exception as e:
        print(f"   Error verifying NumPy: {e}")
        return False

def main():
    """Main function"""
    print("LispCanvas Automatic NumPy Fixer")
    print("This script will automatically fix NumPy compatibility issues")
    
    try:
        success = fix_numpy_issue()
        if success:
            print("\n" + "=" * 50)
            print("SUCCESS! NumPy issue has been fixed.")
            print("You can now run your LispCanvas application without the NumPy error.")
            print("=" * 50)
        else:
            print("\n" + "=" * 50)
            print("FAILED to fix NumPy issue.")
            print("Please try running the quick_fix_numpy.bat script manually.")
            print("=" * 50)
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main()