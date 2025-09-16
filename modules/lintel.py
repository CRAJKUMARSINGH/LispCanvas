import streamlit as st
import numpy as np
import ezdxf
from io import BytesIO
import math

def page_lintel():
    st.title("Lintel Beam Designer")
    
    with st.sidebar:
        st.header("Lintel Design Parameters")
        
        # Basic Dimensions
        st.subheader("Lintel Dimensions")
        span = st.number_input("Clear Span (mm)", min_value=500.0, value=1200.0, step=50.0)
        width = st.number_input("Width (mm)", min_value=100.0, value=200.0, step=10.0)
        depth = st.number_input("Depth (mm)", min_value=150.0, value=250.0, step=10.0)
        
        # Opening Details
        st.subheader("Opening Details")
        opening_type = st.selectbox("Opening Type", ["Door", "Window", "Arch"])
        opening_width = st.number_input("Opening Width (mm)", min_value=500.0, value=1000.0, step=50.0)
        opening_height = st.number_input("Opening Height (mm)", min_value=600.0, value=2100.0, step=50.0)
        
        # Wall Details
        st.subheader("Wall Details")
        wall_thickness = st.number_input("Wall Thickness (mm)", min_value=100.0, value=230.0, step=10.0)
        bearing_length = st.number_input("Bearing Length each side (mm)", min_value=100.0, value=150.0, step=10.0)
        
        # Material Properties
        st.subheader("Material Properties")
        concrete_grade = st.selectbox("Concrete Grade", ["M15", "M20", "M25", "M30"])
        steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"])
        
        # Loads
        st.subheader("Loads")
        wall_load = st.number_input("Wall Load above (kN/m)", min_value=0.0, value=15.0, step=1.0)
        floor_load = st.number_input("Floor Load (kN/m)", min_value=0.0, value=10.0, step=1.0)
        live_load = st.number_input("Live Load (kN/m)", min_value=0.0, value=3.0, step=0.5)
        
        # Reinforcement
        st.subheader("Reinforcement")
        main_bar_dia = st.number_input("Main Bar Diameter (mm)", min_value=8.0, value=12.0, step=2.0)
        num_main_bars = st.number_input("Number of Main Bars", min_value=2, value=3, step=1)
        stirrup_dia = st.number_input("Stirrup Diameter (mm)", min_value=6.0, value=8.0, step=1.0)
        stirrup_spacing = st.number_input("Stirrup Spacing (mm)", min_value=100.0, value=150.0, step=25.0)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Design Summary")
        st.write(f"**Lintel Span:** {span} mm")
        st.write(f"**Lintel Size:** {width} x {depth} mm")
        st.write(f"**Opening:** {opening_width} x {opening_height} mm")
        st.write(f"**Opening Type:** {opening_type}")
        st.write(f"**Wall Thickness:** {wall_thickness} mm")
        st.write(f"**Bearing Length:** {bearing_length} mm each side")
        
        # Basic calculations
        effective_span = span
        total_length = span + (2 * bearing_length)
        
        st.write(f"**Effective Span:** {effective_span} mm")
        st.write(f"**Total Length:** {total_length} mm")
        
        # Load calculations
        total_udl = wall_load + floor_load + live_load
        max_moment = (total_udl * (effective_span/1000)**2) / 8  # kNm
        max_shear = (total_udl * effective_span/1000) / 2  # kN
        
        st.write(f"**Total UDL:** {total_udl:.1f} kN/m")
        st.write(f"**Max Moment:** {max_moment:.1f} kNm")
        st.write(f"**Max Shear:** {max_shear:.1f} kN")
    
    with col2:
        st.subheader("Reinforcement Details")
        st.write(f"**Main Bars:** {num_main_bars} - ø{main_bar_dia} mm")
        st.write(f"**Stirrups:** ø{stirrup_dia} mm @ {stirrup_spacing} mm c/c")
        
        # Steel calculations
        main_steel_area = num_main_bars * math.pi * (main_bar_dia/2)**2
        steel_percentage = (main_steel_area / (width * depth)) * 100
        
        st.write(f"**Main Steel Area:** {main_steel_area:.0f} mm²")
        st.write(f"**Steel Percentage:** {steel_percentage:.2f}%")
        
        # Check minimum steel
        min_steel_req = 0.85 * width * depth / 100  # 0.85% minimum
        if main_steel_area >= min_steel_req:
            st.success("✓ Steel requirement satisfied")
        else:
            st.warning(f"⚠ Need minimum {min_steel_req:.0f} mm² steel")
        
        st.subheader("Material Grades")
        st.write(f"**Concrete:** {concrete_grade}")
        st.write(f"**Steel:** {steel_grade}")
        
        # Concrete volume
        concrete_volume = (width * depth * total_length) / 1000000000  # m³
        st.write(f"**Concrete Volume:** {concrete_volume:.3f} m³")
    
    # Design checks
    st.subheader("Design Checks")
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("**Span to Depth Ratio:**")
        span_depth_ratio = effective_span / depth
        allowable_ratio = 20  # Basic span/depth ratio
        st.write(f"Actual: {span_depth_ratio:.1f}")
        st.write(f"Allowable: {allowable_ratio}")
        if span_depth_ratio <= allowable_ratio:
            st.success("✓ Span/depth ratio OK")
        else:
            st.warning("⚠ Increase depth")
    
    with col4:
        st.write("**Bearing Check:**")
        bearing_stress = (max_shear * 1000) / (width * bearing_length)  # N/mm²
        allowable_bearing = 5.0  # N/mm² for masonry
        st.write(f"Bearing stress: {bearing_stress:.1f} N/mm²")
        st.write(f"Allowable: {allowable_bearing} N/mm²")
        if bearing_stress <= allowable_bearing:
            st.success("✓ Bearing stress OK")
        else:
            st.warning("⚠ Increase bearing length")
    
    # Generate DXF button
    if st.button("Generate DXF Drawing"):
        dxf_content = generate_lintel_dxf(
            span, width, depth, opening_width, opening_height,
            wall_thickness, bearing_length, total_length,
            main_bar_dia, num_main_bars, stirrup_dia, stirrup_spacing
        )
        
        st.download_button(
            label="Download DXF File",
            data=dxf_content,
            file_name="lintel_beam.dxf",
            mime="application/dxf"
        )
        st.success("DXF file generated successfully!")

def generate_lintel_dxf(span, width, depth, opening_width, opening_height,
                       wall_thickness, bearing_length, total_length,
                       main_dia, num_main, stirrup_dia, stirrup_spacing):
    """Generate DXF for lintel beam"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Scale factor
    scale = 0.01
    
    # Convert dimensions to drawing units
    span_scaled = span * scale
    width_scaled = width * scale
    depth_scaled = depth * scale
    total_len_scaled = total_length * scale
    opening_w_scaled = opening_width * scale
    opening_h_scaled = opening_height * scale
    wall_t_scaled = wall_thickness * scale
    
    # Draw elevation view (main view)
    # Wall outline
    wall_left = -bearing_length * scale
    wall_right = (span + bearing_length) * scale
    wall_bottom = 0
    wall_top = opening_height * scale + depth_scaled + 500 * scale  # Wall above lintel
    
    # Draw wall
    msp.add_lwpolyline([
        (wall_left, wall_bottom),
        (wall_right, wall_bottom),
        (wall_right, wall_top),
        (wall_left, wall_top),
        (wall_left, wall_bottom)
    ])
    
    # Draw opening
    opening_left = 0
    opening_right = span_scaled
    opening_bottom = 0
    opening_top = opening_h_scaled
    
    msp.add_lwpolyline([
        (opening_left, opening_bottom),
        (opening_right, opening_bottom),
        (opening_right, opening_top),
        (opening_left, opening_top),
        (opening_left, wall_bottom)
    ])
    
    # Draw lintel beam
    lintel_left = -bearing_length * scale
    lintel_right = (span + bearing_length) * scale
    lintel_bottom = opening_h_scaled
    lintel_top = opening_h_scaled + depth_scaled
    
    msp.add_lwpolyline([
        (lintel_left, lintel_bottom),
        (lintel_right, lintel_bottom),
        (lintel_right, lintel_top),
        (lintel_left, lintel_top),
        (lintel_left, lintel_bottom)
    ])
    
    # Draw reinforcement representation
    # Main bars
    cover = 25 * scale
    bar_y = lintel_bottom + cover
    bar_spacing = (span_scaled - 2 * cover) / max(1, num_main - 1) if num_main > 1 else 0
    
    for i in range(num_main):
        bar_x = cover + (i * bar_spacing) if num_main > 1 else span_scaled / 2
        msp.add_circle((bar_x, bar_y), main_dia * scale / 4)
    
    # Stirrups representation
    stirrup_positions = np.arange(stirrup_spacing * scale, span_scaled, stirrup_spacing * scale)
    for pos in stirrup_positions:
        # Simple stirrup representation as rectangle
        stirrup_pts = [
            (pos - stirrup_dia * scale / 2, lintel_bottom + cover),
            (pos + stirrup_dia * scale / 2, lintel_bottom + cover),
            (pos + stirrup_dia * scale / 2, lintel_top - cover),
            (pos - stirrup_dia * scale / 2, lintel_top - cover),
            (pos - stirrup_dia * scale / 2, lintel_bottom + cover)
        ]
        msp.add_lwpolyline(stirrup_pts)
    
    # Plan view (offset to the right)
    plan_offset_x = total_len_scaled + 1000 * scale
    
    # Draw plan view of lintel
    plan_pts = [
        (plan_offset_x, 0),
        (plan_offset_x + total_len_scaled, 0),
        (plan_offset_x + total_len_scaled, width_scaled),
        (plan_offset_x, width_scaled),
        (plan_offset_x, 0)
    ]
    msp.add_lwpolyline(plan_pts)
    
    # Show main bars in plan
    for i in range(num_main):
        bar_x = plan_offset_x + cover + (i * bar_spacing) if num_main > 1 else plan_offset_x + total_len_scaled / 2
        bar_y = width_scaled / 2
        msp.add_circle((bar_x, bar_y), main_dia * scale / 4)
    
    # Add dimensions and labels
    msp.add_text(f"LINTEL BEAM {width}x{depth}mm", 
                dxfattribs={'height': 100 * scale, 'insert': (span_scaled/2, lintel_top + 200 * scale)})
    
    msp.add_text(f"SPAN = {span}mm", 
                dxfattribs={'height': 50 * scale, 'insert': (span_scaled/2, lintel_bottom - 100 * scale)})
    
    msp.add_text(f"{num_main}-ø{main_dia}mm MAIN BARS", 
                dxfattribs={'height': 40 * scale, 'insert': (span_scaled/2, lintel_bottom - 200 * scale)})
    
    msp.add_text(f"ø{stirrup_dia}mm STIRRUPS @ {stirrup_spacing}mm c/c", 
                dxfattribs={'height': 40 * scale, 'insert': (span_scaled/2, lintel_bottom - 300 * scale)})
    
    # Plan view label
    msp.add_text("PLAN", 
                dxfattribs={'height': 80 * scale, 'insert': (plan_offset_x + total_len_scaled/2, width_scaled + 100 * scale)})
    
    # Save to bytes
    buffer = BytesIO()
    doc.write(buffer)
    return buffer.getvalue()
