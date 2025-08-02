import streamlit as st
import ezdxf
import math
from io import BytesIO

def page_l_beam():
    st.title("L-Beam Designer")
    
    with st.sidebar:
        st.header("Beam Dimensions")
        
        # Flange Dimensions
        st.subheader("Flange (Slab) Dimensions")
        bf = st.number_input("Effective Flange Width (mm)", min_value=300, value=900, step=50)
        tf = st.number_input("Flange Thickness (mm)", min_value=50, value=100, step=10)
        
        # Web Dimensions
        st.subheader("Web Dimensions")
        bw = st.number_input("Web Width (mm)", min_value=100, value=230, step=10)
        d = st.number_input("Effective Depth (mm)", min_value=200, value=400, step=10)
        D = d + st.number_input("Clear Cover (mm)", min_value=15, value=25, step=5) + 10  # 10mm for half bar dia
        
        # Span
        st.subheader("Span & Support")
        L = st.number_input("Effective Span (m)", min_value=1.0, value=4.5, step=0.5)
        support_type = st.selectbox("Support Type", ["Simply Supported", "Continuous"])
        flange_position = st.radio("Flange Position", ["Top Left", "Top Right"])
        
        # Material Properties
        st.subheader("Material Properties")
        fck = st.number_input("fck (N/mm²)", min_value=15, value=20, step=5)
        fy = st.number_input("fy (N/mm²)", min_value=415, value=415, step=100, help="Characteristic strength of steel")
        
        # Loads
        st.subheader("Loads")
        dead_load = st.number_input("Dead Load (kN/m)", min_value=1.0, value=8.0, step=0.5)
        live_load = st.number_input("Live Load (kN/m)", min_value=1.0, value=12.0, step=0.5)
        
        # Reinforcement
        st.subheader("Reinforcement")
        main_bars_dia = st.number_input("Main Bars Diameter (mm)", min_value=10, value=16, step=2)
        num_bars = st.number_input("Number of Tension Bars", min_value=2, value=3, step=1)
        stirrup_dia = st.number_input("Stirrup Diameter (mm)", min_value=6, value=8, step=2)
        stirrup_spacing = st.number_input("Stirrup Spacing (mm)", min_value=50, value=150, step=10)
    
    # Calculate design parameters
    total_load = 1.5 * (dead_load + live_load)  # Factored load
    
    if support_type == "Simply Supported":
        max_moment = (total_load * L**2) / 8  # kNm
        max_shear = (total_load * L) / 2  # kN
    else:  # Continuous
        max_moment = (total_load * L**2) / 10  # Approximate for continuous
        max_shear = 0.6 * total_load * L  # Approximate for continuous
    
    # Display design summary
    st.header("Design Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Geometry")
        st.write(f"- Effective Span: {L} m")
        st.write(f"- Flange Width: {bf} mm")
        st.write(f"- Flange Thickness: {tf} mm")
        st.write(f"- Web Width: {bw} mm")
        st.write(f"- Overall Depth: {D} mm")
        st.write(f"- Effective Depth: {d} mm")
        st.write(f"- Flange Position: {flange_position}")
        
    with col2:
        st.subheader("Design Forces")
        st.write(f"- Total Factored Load: {total_load:.2f} kN/m")
        st.write(f"- Maximum Bending Moment: {max_moment:.2f} kNm")
        st.write(f"- Maximum Shear Force: {max_shear:.2f} kN")
        st.write(f"- Concrete Grade: M{fck}")
        st.write(f"- Steel Grade: Fe{fy}")
    
    # DXF Generation
    if st.button("Generate DXF Drawing"):
        dxf_bytes = generate_l_beam_dxf(bf, tf, bw, D, d, main_bars_dia, num_bars, 
                                     stirrup_dia, stirrup_spacing, flange_position)
        
        # Download button
        st.download_button(
            label="Download L-Beam DXF",
            data=dxf_bytes,
            file_name=f"l_beam_{int(bf)}x{int(D)}_{flange_position.replace(' ', '_')}.dxf",
            mime="application/dxf"
        )
        
        st.success("L-Beam DXF generated successfully!")
    
    # Design Calculations
    with st.expander("Design Calculations", expanded=False):
        st.subheader("Section Properties")
        area = (bf * tf) + ((D - tf) * bw)
        st.write(f"- Cross-sectional Area: {area / 1e6:.3f} m²")
        st.write(f"- Self Weight: {25 * area / 1e6:.2f} kN/m")
        
        st.subheader("Bending Design")
        xu_lim = 0.48 * d  # For Fe415 and M20 concrete
        st.write(f"- Limiting Neutral Axis Depth: {xu_lim:.1f} mm")
        
        st.write("\n**Moment Capacity Check**")
        st.write("Assuming balanced section:")
        st.write(f"- Moment of Resistance (Mu_lim) = 0.36 * fck * xu_lim * b * (d - 0.42 * xu_lim)")
        
        st.subheader("Shear Design")
        st.write(f"- Nominal Shear Stress (τv) = {max_shear * 1000 / (bw * d):.2f} N/mm²")
        st.write(f"- Minimum Shear Reinforcement Required: {0.4 * bw * stirrup_spacing / (0.87 * fy):.2f} mm²")
    
    # Construction Notes
    with st.expander("Construction Notes", expanded=False):
        st.write("1. All dimensions are in millimeters unless specified otherwise.")
        st.write(f"2. Concrete grade: M{fck}")
        st.write(f"3. Steel grade: Fe{fy}")
        st.write("4. Clear cover: 25mm (adjust as per exposure conditions)")
        st.write("5. Provide adequate anchorage for main bars into supports")
        st.write("6. Ensure proper compaction at web-flange junction")
        st.write("7. Provide additional top reinforcement in flange for negative moments")

def generate_l_beam_dxf(bf, tf, bw, D, d, main_bars_dia, num_bars, stirrup_dia, stirrup_spacing, flange_position):
    """Generate DXF file for L-Beam section."""
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()
    
    # Define layers
    doc.layers.new(name='OUTLINE', dxfattribs={'color': 1})
    doc.layers.new(name='REINFORCEMENT', dxfattribs={'color': 1})
    doc.layers.new(name='DIMENSIONS', dxfattribs={'color': 4})
    doc.layers.new(name='TEXT', dxfattribs={'color': 7})
    
    # Draw L-Beam outline based on flange position
    if flange_position == "Top Left":
        points = [
            (0, 0),
            (bw, 0),
            (bw, D),
            (bf + bw, D),
            (bf + bw, D - tf),
            (bw, D - tf),
            (bw, 0),
            (0, 0)
        ]
    else:  # Top Right
        points = [
            (0, 0),
            (bw, 0),
            (bw, D - tf),
            (0, D - tf),
            (0, D),
            (bw + bf, D),
            (bw + bf, 0),
            (bw, 0)
        ]
    
    msp.add_lwpolyline(points, dxfattribs={'layer': 'OUTLINE'})
    
    # Draw centerline
    web_center = bw/2 if flange_position == "Top Left" else (bw + bf)/2
    msp.add_line((web_center, 0), (web_center, D), dxfattribs={'layer': 'CENTER', 'linetype': 'DASHED'})
    
    # Draw reinforcement
    cover = 25  # mm
    bar_radius = main_bars_dia / 2
    
    # Main tension bars
    if flange_position == "Top Left":
        bar_x_start = cover + bar_radius
        bar_x_end = bw - cover - bar_radius
        bar_y = D - cover - bar_radius
        
        # Distribute bars in web
        if num_bars > 1:
            bar_spacing = (bar_x_end - bar_x_start) / (num_bars - 1)
            for i in range(num_bars):
                x = bar_x_start + (i * bar_spacing)
                msp.add_circle((x, bar_y), bar_radius, dxfattribs={'layer': 'REINFORCEMENT'})
        else:
            msp.add_circle((bw/2, bar_y), bar_radius, dxfattribs={'layer': 'REINFORCEMENT'})
    else:  # Top Right
        bar_x_start = bw + cover + bar_radius
        bar_x_end = bw + bf - cover - bar_radius
        bar_y = D - cover - bar_radius
        
        # Distribute bars in flange
        if num_bars > 1:
            bar_spacing = (bar_x_end - bar_x_start) / (num_bars - 1)
            for i in range(num_bars):
                x = bar_x_start + (i * bar_spacing)
                msp.add_circle((x, bar_y), bar_radius, dxfattribs={'layer': 'REINFORCEMENT'})
        else:
            msp.add_circle((bw + bf/2, bar_y), bar_radius, dxfattribs={'layer': 'REINFORCEMENT'})
    
    # Draw stirrups
    stirrup_width = bw - 2*cover - stirrup_dia
    stirrup_height = D - 2*cover - stirrup_dia
    
    # Draw stirrups at critical sections (supports and midspan)
    for x_offset in [0, L*1000/4, L*1000/2]:  # Start, quarter, and mid-span
        if flange_position == "Top Left":
            x = cover + stirrup_dia/2 + x_offset
            points = [
                (x, cover + stirrup_dia/2),
                (x + stirrup_width, cover + stirrup_dia/2),
                (x + stirrup_width, cover + stirrup_dia/2 + stirrup_height),
                (x, cover + stirrup_dia/2 + stirrup_height),
                (x, cover + stirrup_dia/2)
            ]
        else:  # Top Right
            x = cover + stirrup_dia/2 + x_offset
            points = [
                (x, cover + stirrup_dia/2),
                (x + stirrup_width, cover + stirrup_dia/2),
                (x + stirrup_width, cover + stirrup_dia/2 + stirrup_height),
                (x, cover + stirrup_dia/2 + stirrup_height),
                (x, cover + stirrup_dia/2)
            ]
        msp.add_lwpolyline(points, dxfattribs={'layer': 'REINFORCEMENT'})
    
    # Add dimensions
    if flange_position == "Top Left":
        # Overall width dimension
        msp.add_aligned_dim(
            p1=(0, -50),
            p2=(bw + bf, -50),
            distance=-100,
            dimstyle='EZDXF',
            override={
                'dimtxsty': 'Standard',
                'dimtxt': 2.5,
                'dimgap': 1.0,
                'dimscale': 1.0
            }
        )
    else:  # Top Right
        msp.add_aligned_dim(
            p1=(0, -50),
            p2=(bw + bf, -50),
            distance=-100,
            dimstyle='EZDXF',
            override={
                'dimtxsty': 'Standard',
                'dimtxt': 2.5,
                'dimgap': 1.0,
                'dimscale': 1.0
            }
        )
    
    # Height dimension
    msp.add_aligned_dim(
        p1=(-50, 0),
        p2=(-50, D),
        distance=-100,
        dimstyle='EZDXF',
        override={
            'dimtxsty': 'Standard',
            'dimtxt': 2.5,
            'dimgap': 1.0,
            'dimscale': 1.0
        }
    )
    
    # Add section information
    info = [
        f"L-BEAM SECTION - {flange_position.upper()}",
        f"Flange: {bf} x {tf} mm",
        f"Web: {bw} x {D} mm",
        f"Main Bars: {num_bars} - Ø{main_bars_dia} mm",
        f"Stirrups: Ø{stirrup_dia} mm @ {stirrup_spacing} mm c/c"
    ]
    
    y_offset = -150
    for i, text in enumerate(info):
        msp.add_text(
            text,
            dxfattribs={
                'height': 2.5 if i == 0 else 2.0,
                'layer': 'TEXT'
            }
        ).set_pos(((bw + bf)/2, y_offset - i * 7), align='MIDDLE_CENTER')
    
    # Save to bytes and return
    dxf_bytes = BytesIO()
    doc.saveas(dxf_bytes)
    dxf_bytes.seek(0)
    return dxf_bytes
