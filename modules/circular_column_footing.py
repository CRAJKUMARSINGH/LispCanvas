import streamlit as st
import numpy as np
import ezdxf
from io import BytesIO
import math

def page_circular_column_footing():
    st.title("Circular Column with Footing Designer")
    
    with st.sidebar:
        st.header("Design Parameters")
        
        # Column Dimensions
        st.subheader("Column Dimensions")
        col_diameter = st.number_input("Column Diameter (mm)", min_value=150.0, value=300.0, step=10.0)
        col_height = st.number_input("Column Height (mm)", min_value=1000.0, value=3000.0, step=100.0)
        
        # Footing Dimensions  
        st.subheader("Footing Dimensions")
        footing_diameter = st.number_input("Footing Diameter (mm)", min_value=500.0, value=1200.0, step=50.0)
        footing_thickness = st.number_input("Footing Thickness (mm)", min_value=200.0, value=400.0, step=25.0)
        
        # Material Properties
        st.subheader("Material Properties")
        concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40"])
        steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"])
        
        # Reinforcement Details
        st.subheader("Column Reinforcement")
        main_bars_dia = st.number_input("Main Bars Diameter (mm)", min_value=8.0, value=16.0, step=2.0)
        num_main_bars = st.number_input("Number of Main Bars", min_value=4, value=8, step=1)
        tie_dia = st.number_input("Ties Diameter (mm)", min_value=6.0, value=8.0, step=1.0)
        tie_spacing = st.number_input("Tie Spacing (mm)", min_value=100.0, value=150.0, step=10.0)
        
        st.subheader("Footing Reinforcement")
        footing_bar_dia = st.number_input("Footing Bar Diameter (mm)", min_value=8.0, value=12.0, step=2.0)
        footing_bar_spacing = st.number_input("Footing Bar Spacing (mm)", min_value=100.0, value=150.0, step=10.0)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Design Summary")
        st.write(f"**Column Diameter:** {col_diameter} mm")
        st.write(f"**Column Height:** {col_height} mm")
        st.write(f"**Footing Diameter:** {footing_diameter} mm")
        st.write(f"**Footing Thickness:** {footing_thickness} mm")
        st.write(f"**Concrete Grade:** {concrete_grade}")
        st.write(f"**Steel Grade:** {steel_grade}")
        
        # Basic calculations
        col_area = math.pi * (col_diameter/2)**2
        footing_area = math.pi * (footing_diameter/2)**2
        footing_volume = footing_area * footing_thickness / 1000000000  # m³
        
        st.write(f"**Column Area:** {col_area:.0f} mm²")
        st.write(f"**Footing Area:** {footing_area:.0f} mm²")
        st.write(f"**Footing Concrete Volume:** {footing_volume:.2f} m³")
    
    with col2:
        st.subheader("Reinforcement Details")
        st.write("**Column Reinforcement:**")
        st.write(f"- Main Bars: {num_main_bars} - Ø{main_bars_dia} mm")
        st.write(f"- Ties: Ø{tie_dia} mm @ {tie_spacing} mm c/c")
        
        st.write("**Footing Reinforcement:**")
        st.write(f"- Bars: Ø{footing_bar_dia} mm @ {footing_bar_spacing} mm c/c both ways")
        
        # Steel calculations
        main_steel_length = col_height + 600  # Development length
        main_steel_weight = (main_steel_length * num_main_bars * (main_bars_dia**2) * math.pi / 4) * 7850 / 1000000000
        
        footing_bars_each_way = int(footing_diameter / footing_bar_spacing) + 1
        footing_steel_length = footing_bars_each_way * footing_diameter * 2
        footing_steel_weight = (footing_steel_length * (footing_bar_dia**2) * math.pi / 4) * 7850 / 1000000000
        
        st.write(f"**Main Steel Weight:** {main_steel_weight:.1f} kg")
        st.write(f"**Footing Steel Weight:** {footing_steel_weight:.1f} kg")
    
    # Generate DXF button
    if st.button("Generate DXF Drawing"):
        dxf_content = generate_circular_column_footing_dxf(
            col_diameter, col_height, footing_diameter, footing_thickness,
            main_bars_dia, num_main_bars, tie_dia, tie_spacing,
            footing_bar_dia, footing_bar_spacing
        )
        
        st.download_button(
            label="Download DXF File",
            data=dxf_content,
            file_name="circular_column_footing.dxf",
            mime="application/dxf"
        )
        st.success("DXF file generated successfully!")

def generate_circular_column_footing_dxf(col_dia, col_height, foot_dia, foot_thickness,
                                       main_dia, num_main, tie_dia, tie_spacing,
                                       foot_bar_dia, foot_bar_spacing):
    """Generate DXF for circular column with footing"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Scale factor for drawing
    scale = 0.01
    
    # Convert to drawing units
    col_radius = (col_dia * scale) / 2
    col_h = col_height * scale
    foot_radius = (foot_dia * scale) / 2
    foot_h = foot_thickness * scale
    
    # Draw footing (plan view)
    footing_center = (0, 0)
    msp.add_circle(footing_center, foot_radius)
    
    # Draw column (plan view)
    msp.add_circle(footing_center, col_radius)
    
    # Draw elevation view offset
    elev_offset_x = foot_radius * 3
    
    # Footing elevation
    foot_pts = [
        (elev_offset_x - foot_radius, 0),
        (elev_offset_x + foot_radius, 0),
        (elev_offset_x + foot_radius, foot_h),
        (elev_offset_x - foot_radius, foot_h)
    ]
    msp.add_lwpolyline(foot_pts + [foot_pts[0]])
    
    # Column elevation
    col_pts = [
        (elev_offset_x - col_radius, foot_h),
        (elev_offset_x + col_radius, foot_h),
        (elev_offset_x + col_radius, foot_h + col_h),
        (elev_offset_x - col_radius, foot_h + col_h)
    ]
    msp.add_lwpolyline(col_pts + [col_pts[0]])
    
    # Add reinforcement representation
    # Main bars in plan
    angle_step = 360 / num_main
    for i in range(num_main):
        angle = math.radians(i * angle_step)
        bar_x = (col_radius - 25 * scale) * math.cos(angle)
        bar_y = (col_radius - 25 * scale) * math.sin(angle)
        msp.add_circle((bar_x, bar_y), main_dia * scale / 4)
    
    # Add dimensions and text
    msp.add_text(f"COLUMN Ø{col_dia}", 
                dxfattribs={'height': 50 * scale, 'insert': (0, foot_radius + 100 * scale)})
    msp.add_text(f"FOOTING Ø{foot_dia} x {foot_thickness}mm", 
                dxfattribs={'height': 50 * scale, 'insert': (0, foot_radius + 200 * scale)})
    
    # Save to bytes - Fixed the issue here using the correct approach
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as fp:
        temp_filename = fp.name
    doc.saveas(temp_filename)
    with open(temp_filename, 'rb') as f:
        content = f.read()
    os.unlink(temp_filename)
    return content