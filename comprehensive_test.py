"""
Comprehensive test for circular column footing module
"""

def comprehensive_test():
    """Comprehensive test that mimics the app behavior"""
    print("Running comprehensive test...")
    
    try:
        # Import the function exactly as in app.py
        try:
            from modules.circular_column_footing import page_circular_column_footing
            print("✅ Module imported successfully")
        except Exception as e:
            print(f"❌ Module import failed: {e}")
            return False
            
        # Test the DXF generation function directly
        from modules.circular_column_footing import generate_circular_column_footing_dxf
        
        print("Testing DXF generation with sample parameters...")
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
        
        if isinstance(dxf_content, bytes) and len(dxf_content) > 0:
            print(f"✅ DXF generation successful ({len(dxf_content)} bytes)")
        else:
            print(f"❌ DXF generation failed - content type: {type(dxf_content)}, length: {len(dxf_content) if hasattr(dxf_content, '__len__') else 'N/A'}")
            return False
            
        print("✅ Comprehensive test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during comprehensive test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    comprehensive_test()