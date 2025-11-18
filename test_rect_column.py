"""
Test script for rectangular column module
"""

def test_rectangular_column():
    """Test the rectangular column module"""
    print("Testing rectangular column module...")
    
    try:
        # Import the function
        from modules.rectangular_column import page_rectangular_column
        print("✅ Module imported successfully")
        
        # Test the DXF generation function directly
        import inspect
        import os
        
        # Get the source code of the function
        source_lines = inspect.getsource(page_rectangular_column).split('\n')
        print(f"Function has {len(source_lines)} lines")
        
        # Check if there's any doc.write call
        for i, line in enumerate(source_lines):
            if 'doc.write' in line:
                print(f"❌ Found doc.write in line {i+1}: {line}")
                return False
                
        print("✅ No doc.write calls found in function")
        print("✅ Test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_rectangular_column()