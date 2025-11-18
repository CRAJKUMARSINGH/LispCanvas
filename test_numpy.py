"""
Test script to verify NumPy installation and functionality
"""

import sys
import os

def test_numpy_import():
    """Test NumPy import and basic functionality"""
    print("Testing NumPy installation...")
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
        print(f"NumPy version: {np.__version__}")
        
        # Test basic NumPy functionality
        arr = np.array([1, 2, 3, 4, 5])
        print(f"✅ Basic array creation works: {arr}")
        
        # Test mathematical operations
        result = np.pi * (10/2)**2
        print(f"✅ Mathematical operations work: π * (10/2)² = {result:.2f}")
        
        # Test multiarray functionality
        arr2 = np.array([[1, 2], [3, 4]])
        print(f"✅ Multi-dimensional arrays work: \n{arr2}")
        
        return True
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ NumPy functionality test failed: {e}")
        return False

def test_module_specific_numpy():
    """Test NumPy usage in specific modules"""
    print("\nTesting module-specific NumPy usage...")
    
    modules_to_test = [
        ("Sunshade", "modules.sunshade"),
        ("Circular Column", "modules.circular_column"),
        ("Rectangular Column", "modules.rectangular_column")
    ]
    
    results = []
    for module_name, module_path in modules_to_test:
        try:
            # Import the module
            module = __import__(module_path, fromlist=[''])
            print(f"✅ {module_name} module imported successfully")
            
            # Test that NumPy is accessible within the module
            if hasattr(module, 'np'):
                # Test a simple NumPy operation from within the module context
                result = module.np.pi * (10/2)**2
                print(f"✅ {module_name} NumPy usage works: π * (10/2)² = {result:.2f}")
            else:
                print(f"⚠️  {module_name} doesn't have direct np reference, but module imports")
            
            results.append(True)
        except Exception as e:
            print(f"❌ {module_name} NumPy test failed: {e}")
            results.append(False)
    
    return all(results)

def main():
    """Run all NumPy tests"""
    print("=" * 50)
    print("NUMPY FUNCTIONALITY VERIFICATION")
    print("=" * 50)
    
    # Test basic NumPy functionality
    basic_test = test_numpy_import()
    
    # Test module-specific NumPy usage
    module_test = test_module_specific_numpy()
    
    print("\n" + "=" * 50)
    if basic_test and module_test:
        print("✅ ALL NUMPY TESTS PASSED")
        print("NumPy should work correctly in the application")
    else:
        print("❌ SOME NUMPY TESTS FAILED")
        print("There may be issues with the NumPy installation")
    print("=" * 50)

if __name__ == "__main__":
    main()