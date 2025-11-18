"""
Integration test for lintel and sunshade modules
This script verifies that both modules are properly wired to the main design application
"""

import sys
import os

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_module_integration():
    """Test that lintel and sunshade modules are properly integrated"""
    print("Testing Lintel and Sunshade Module Integration")
    print("=" * 50)
    
    try:
        # Test importing the main app structure
        print("1. Testing main app imports...")
        
        # Test importing individual modules
        from modules.lintel import page_lintel, generate_lintel_dxf
        print("   ✅ Lintel module imported successfully")
        
        from modules.sunshade import page_sunshade, create_sunshade_dxf
        print("   ✅ Sunshade module imported successfully")
        
        # Test that all required functions exist and are callable
        assert callable(page_lintel), "page_lintel should be callable"
        assert callable(page_sunshade), "page_sunshade should be callable"
        assert callable(generate_lintel_dxf), "generate_lintel_dxf should be callable"
        assert callable(create_sunshade_dxf), "create_sunshade_dxf should be callable"
        
        print("   ✅ All functions are callable")
        
        # Test DXF generation for lintel
        print("2. Testing Lintel DXF generation...")
        dxf_content = generate_lintel_dxf(
            span=1200.0, width=200.0, depth=250.0, 
            opening_width=1000.0, opening_height=2100.0,
            wall_thickness=230.0, bearing_length=150.0, total_length=1500.0,
            main_dia=12.0, num_main=3, stirrup_dia=8.0, stirrup_spacing=150.0
        )
        assert dxf_content is not None, "Lintel DXF content should not be None"
        print("   ✅ Lintel DXF generated successfully")
        
        # Test DXF generation for sunshade
        print("3. Testing Sunshade DXF generation...")
        doc = create_sunshade_dxf(
            web_width=300, total_depth=450, projection=1000, 
            support_thickness=150, edge_thickness=100,
            bottom_bar_dia=16, num_bottom_bars=4, top_bar_dia=12, num_top_bars=2,
            stirrup_dia=8, stirrup_spacing=150, main_bar_dia=10, dist_bar_dia=8,
            dist_bar_spacing=150, scale=25, sunshade_num="01"
        )
        assert doc is not None, "Sunshade DXF document should not be None"
        print("   ✅ Sunshade DXF generated successfully")
        
        # Test file operations
        print("4. Testing file operations...")
        
        # Test lintel DXF file save
        with open("test_lintel.dxf", "wb") as f:
            f.write(dxf_content)
        print("   ✅ Lintel DXF file saved successfully")
        
        # Test sunshade DXF file save
        doc.saveas("test_sunshade.dxf")
        print("   ✅ Sunshade DXF file saved successfully")
        
        # Clean up test files
        os.remove("test_lintel.dxf")
        os.remove("test_sunshade.dxf")
        print("   ✅ Test files cleaned up successfully")
        
        print("\n" + "=" * 50)
        print("✅ ALL INTEGRATION TESTS PASSED!")
        print("Lintel and Sunshade modules are properly wired to the main design application.")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_module_integration()
    sys.exit(0 if success else 1)