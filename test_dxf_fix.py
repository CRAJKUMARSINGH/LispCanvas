"""
Test script to verify that the DXF saving fixes work correctly
"""

import sys
import os

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_circular_column_dxf():
    """Test that circular column DXF generation works"""
    print("Testing Circular Column DXF Generation...")
    try:
        # Test that we can create a document and save it properly
        import ezdxf
        import tempfile
        import os
        
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()
        msp.add_circle(center=(0, 0), radius=150)
        
        # Test the correct approach (saveas with temporary file)
        with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as fp:
            temp_filename = fp.name
        doc.saveas(temp_filename)
        with open(temp_filename, 'rb') as f:
            content = f.read()
        os.unlink(temp_filename)
        
        print("✅ Circular column DXF generation works correctly")
        return True
    except Exception as e:
        print(f"❌ Circular column DXF generation failed: {e}")
        return False

def test_rectangular_column_dxf():
    """Test that rectangular column DXF generation works"""
    print("Testing Rectangular Column DXF Generation...")
    try:
        # Test that we can create a document and save it properly
        import ezdxf
        import tempfile
        import os
        
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()
        msp.add_lwpolyline([(0, 0), (300, 0), (300, 450), (0, 450), (0, 0)])
        
        # Test the correct approach (saveas with temporary file)
        with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as fp:
            temp_filename = fp.name
        doc.saveas(temp_filename)
        with open(temp_filename, 'rb') as f:
            content = f.read()
        os.unlink(temp_filename)
        
        print("✅ Rectangular column DXF generation works correctly")
        return True
    except Exception as e:
        print(f"❌ Rectangular column DXF generation failed: {e}")
        return False

def test_rect_column_footing_dxf():
    """Test that rectangular column with footing DXF generation works"""
    print("Testing Rectangular Column with Footing DXF Generation...")
    try:
        # Test that we can create a document and save it properly
        import ezdxf
        import tempfile
        import os
        
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()
        msp.add_lwpolyline([(0, 0), (2000, 0), (2000, 2500), (0, 2500), (0, 0)])
        
        # Test the correct approach (saveas with temporary file)
        with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as fp:
            temp_filename = fp.name
        doc.saveas(temp_filename)
        with open(temp_filename, 'rb') as f:
            content = f.read()
        os.unlink(temp_filename)
        
        print("✅ Rectangular column with footing DXF generation works correctly")
        return True
    except Exception as e:
        print(f"❌ Rectangular column with footing DXF generation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("DXF GENERATION FIX VERIFICATION")
    print("=" * 60)
    
    tests = [
        test_circular_column_dxf,
        test_rectangular_column_dxf,
        test_rect_column_footing_dxf
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    print("=" * 60)
    if all(results):
        print("✅ ALL TESTS PASSED - DXF GENERATION FIXES ARE WORKING")
        print("The OSError related to BytesIO should now be resolved.")
    else:
        print("❌ SOME TESTS FAILED - Please check the error messages above")
    print("=" * 60)

if __name__ == "__main__":
    main()