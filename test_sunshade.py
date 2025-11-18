import sys
import os

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from modules.sunshade import page_sunshade
    print("Sunshade module imported successfully")
    
    # Test if we can create a DXF document
    from utils.dxf_utils import create_dxf_header
    doc = create_dxf_header()
    print("DXF document created successfully")
    
    # Test if we can save the document
    doc.saveas("test_sunshade.dxf")
    print("DXF document saved successfully")
    
    # Clean up
    os.remove("test_sunshade.dxf")
    print("Test file cleaned up")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Sunshade test completed")