import ezdxf

def create_dxf_header():
    """Create a new DXF document with standard header settings"""
    doc = ezdxf.new('R2010')
    doc.header['$INSUNITS'] = 4  # Millimeters
    return doc

def add_dimensions(msp, points, scale_factor=1.0):
    """Add dimension lines to the drawing"""
    # This is a placeholder function - implement as needed
    pass

def add_text(msp, text, insert_point, height=2.5, scale_factor=1.0):
    """Add text to the drawing"""
    scaled_height = height * scale_factor
    scaled_insert = (insert_point[0] * scale_factor, insert_point[1] * scale_factor)
    msp.add_text(text, dxfattribs={'height': scaled_height}).set_placement(scaled_insert)