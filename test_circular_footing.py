"""
Test script for circular column footing DXF generation
"""

def test_circular_column_footing_dxf():
    """Test the circular column footing DXF generation"""
    print("Testing circular column footing DXF generation...")
    
    try:
        # Import the function
        from modules.circular_column_footing import generate_circular_column_footing_dxf
        
        # Test with sample parameters
        dxf_content = generate_circular_column_footing_dxf(
            col_dia=300.0,
            col_height=3000.0,
            foot_dia=1200.0,
            foot_thickness=400.0,
            main_dia=16.0,
            num_main=8,
            tie_dia=8.0,
            tie_spacing=150.0,
            foot_bar_dia=12.0,
            foot_bar_spacing=150.0
        )
        
        # Check if content is bytes
        if isinstance(dxf_content, bytes):
            print(f"✅ DXF content generated successfully ({len(dxf_content)} bytes)")
            print("✅ Content type is bytes (correct)")
        else:
            print(f"❌ Content type is {type(dxf_content)}, expected bytes")
            return False
            
        # Check if content is not empty
        if len(dxf_content) > 0:
            print("✅ DXF content is not empty")
        else:
            print("❌ DXF content is empty")
            return False
            
        print("✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_circular_column_footing_dxf()