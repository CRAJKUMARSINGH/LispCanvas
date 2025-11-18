import sys
import os

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from modules.lintel import page_lintel, generate_lintel_dxf
    print("Lintel module imported successfully")
    
    # Test if we can create a DXF document
    dxf_content = generate_lintel_dxf(
        span=1200.0, width=200.0, depth=250.0, 
        opening_width=1000.0, opening_height=2100.0,
        wall_thickness=230.0, bearing_length=150.0, total_length=1500.0,
        main_dia=12.0, num_main=3, stirrup_dia=8.0, stirrup_spacing=150.0
    )
    print("Lintel DXF content generated successfully")
    
    # Test if we can save the document
    with open("test_lintel.dxf", "wb") as f:
        f.write(dxf_content)
    print("Lintel DXF document saved successfully")
    
    # Clean up
    os.remove("test_lintel.dxf")
    print("Test file cleaned up")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Lintel test completed")