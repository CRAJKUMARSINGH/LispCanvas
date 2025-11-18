"""
Script to fix NumPy "core.multiarray failed to import" error
This script provides guidance on how to fix the NumPy compatibility issue
"""

import sys
import os

def diagnose_numpy_issue():
    """Diagnose the NumPy issue"""
    print("=" * 60)
    print("NUMPY ISSUE DIAGNOSIS")
    print("=" * 60)
    
    try:
        import numpy as np
        print(f"✅ NumPy is installed (version: {np.__version__})")
        
        # Test basic NumPy functionality
        try:
            result = np.pi * 2
            print(f"✅ Basic NumPy operations work: π * 2 = {result:.2f}")
        except Exception as e:
            print(f"❌ Basic NumPy operations failed: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ NumPy is not installed or cannot be imported: {e}")
        return False
    
    # Check for common incompatible packages
    incompatible_packages = []
    try:
        import pandas as pd
        print(f"✅ Pandas is installed (version: {pd.__version__})")
    except ImportError:
        print("⚠️  Pandas is not installed")
    except Exception as e:
        print(f"❌ Pandas import failed: {e}")
        incompatible_packages.append("pandas")
    
    try:
        import matplotlib
        print(f"✅ Matplotlib is installed (version: {matplotlib.__version__})")
    except ImportError:
        print("⚠️  Matplotlib is not installed")
    except Exception as e:
        print(f"❌ Matplotlib import failed: {e}")
        incompatible_packages.append("matplotlib")
    
    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)
    
    if incompatible_packages:
        print("⚠️  The following packages may have compatibility issues:")
        for package in incompatible_packages:
            print(f"   - {package}")
        return False
    else:
        print("✅ No obvious compatibility issues detected")
        return True

def provide_fix_instructions():
    """Provide instructions to fix the NumPy issue"""
    print("\n" + "=" * 60)
    print("SOLUTION: FIX NUMPY CORE.MULTIARRAY ERROR")
    print("=" * 60)
    
    print("""
The error "numpy.core.multiarray failed to import" is typically caused by 
incompatibility between NumPy 2.x and packages compiled against NumPy 1.x.

Here are the recommended solutions:
""")
    
    print("SOLUTION 1: Downgrade NumPy to version 1.x")
    print("-" * 40)
    print("Run these commands in your terminal:")
    print("  pip uninstall numpy -y")
    print("  pip install numpy==1.24.3")
    print()
    
    print("SOLUTION 2: Reinstall conflicting packages")
    print("-" * 40)
    print("Run these commands in your terminal:")
    print("  pip uninstall numpy pandas matplotlib -y")
    print("  pip install numpy==1.24.3 pandas matplotlib")
    print()
    
    print("SOLUTION 3: Create a fresh virtual environment")
    print("-" * 40)
    print("Run these commands in your terminal:")
    print("  python -m venv lisp_canvas_fix")
    print("  lisp_canvas_fix\\Scripts\\activate  # On Windows")
    print("  pip install -r requirements.txt")
    print()
    
    print("After applying any solution, verify with:")
    print("  python -c \"import numpy as np; print('Success:', np.pi * 2)\"")
    print()
    
    print("For more detailed instructions, see NUMPY_ERROR_SOLUTION.md")

def main():
    """Main function"""
    print("LispCanvas NumPy Issue Fixer")
    print("This script helps diagnose and fix NumPy compatibility issues")
    
    # Diagnose the issue
    diagnosis_result = diagnose_numpy_issue()
    
    # Provide fix instructions
    provide_fix_instructions()
    
    print("\n" + "=" * 60)
    print("RECOMMENDATION")
    print("=" * 60)
    print("The most reliable fix is to downgrade NumPy to version 1.24.3")
    print("This will resolve compatibility issues with existing packages.")

if __name__ == "__main__":
    main()