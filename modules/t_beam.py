import streamlit as st
import ezdxf
import math
from io import BytesIO

def page_t_beam():
    st.title("T-Beam Designer")
    
    with st.sidebar:
        st.header("Beam Dimensions")
        
        # Flange Dimensions
        st.subheader("Flange (Slab) Dimensions")
        bf = st.number_input("Effective Flange Width (mm)", min_value=500, value=1500, step=50)
        tf = st.number_input("Flange Thickness (mm)", min_value=50, value=100, step=10)
        
        # Web Dimensions
        st.subheader("Web Dimensions")
        bw = st.number_input("Web Width (mm)", min_value=100, value=230, step=10)
        d = st.number_input("Effective Depth (mm)", min_value=200, value=400, step=10)
        D = d + st.number_input("Clear Cover (mm)", min_value=15, value=25, step=5) + 10  # 10mm for half bar dia
        
        # Span
        st.subheader("Span & Support")
        L = st.number_input("Effective Span (m)", min_value=1.0, value=5.0, step=0.5)
        support_type = st.selectbox("Support Type", ["Simply Supported", "Continuous"])
        
        # Material Properties
        st.subheader("Material Properties")
        fck = st.number_input("fck (N/mm²)", min_value=15, value=20, step=5)
        fy = st.number_input("fy (N/mm²)", min_value=415, value=415, step=100, help="Characteristic strength of steel")
        
        # Loads
        st.subheader("Loads")
        dead_load = st.number_input("Dead Load (kN/m)", min_value=1.0, value=10.0, step=0.5)
        live_load = st.number_input("Live Load (kN/m)", min_value=1.0, value=15.0, step=0.5)
        
        # Reinforcement
        st.subheader("Reinforcement")
        main_bars_dia = st.number_input("Main Bars Diameter (mm)", min_value=10, value=16, step=2)
        num_bars = st.number_input("Number of Tension Bars", min_value=2, value=4, step=1)
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
        
    with col2:
        st.subheader("Design Forces")
        st.write(f"- Total Factored Load: {total_load:.2f} kN/m")
        st.write(f"- Maximum Bending Moment: {max_moment:.2f} kNm")
        st.write(f"- Maximum Shear Force: {max_shear:.2f} kN")
        st.write(f"- Concrete Grade: M{fck}")
        st.write(f"- Steel Grade: Fe{fy}")
    
    # DXF Generation
    if st.button("Generate DXF Drawing"):
        dxf_bytes = generate_t_beam_dxf(bf, tf, bw, D, d, main_bars_dia, num_bars, stirrup_dia, stirrup_spacing)
        
        # Download button
        st.download_button(
            label="Download T-Beam DXF",
            data=dxf_bytes,
            file_name=f"t_beam_{int(bf)}x{int(D)}.dxf",
            mime="application/dxf"
        )
        
        st.success("T-Beam DXF generated successfully!")
    
    # Design Calculations
    with st.expander("Design Calculations", expanded=False):
        st.subheader("Section Properties")
        st.write(f"- Cross-sectional Area: {((bf * tf) + ((D - tf) * bw)) / 1e6:.3f} m²")
        st.write(f"- Self Weight: {25 * ((bf * tf) + ((D - tf) * bw)) / 1e6:.2f} kN/m")
        
        st.subheader("Bending Design")
        # Simplified design calculations
        xu_lim = 0.48 * d  # For Fe415 and M20 concrete
        st.write(f"- Limiting Neutral Axis Depth: {xu_lim:.1f} mm")
        
        # Moment capacity calculation (simplified)
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
        st.write("5. Development length should be checked as per IS 456:2000")
        st.write("6. Lap splices should be staggered and not located at sections of maximum stress")
        st.write("7. Proper compaction of concrete is essential, especially in the web-flange junction")

def generate_t_beam_dxf(bf, tf, bw, D, d, main_bars_dia, num_bars, stirrup_dia, stirrup_spacing):
    """Generate DXF file for T-Beam section."""
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()
    
    # Define layers
    doc.layers.new(name='OUTLINE', dxfattribs={'color': 1})
    doc.layers.new(name='REINFORCEMENT', dxfattribs={'color': 1})
    doc.layers.new(name='DIMENSIONS', dxfattribs={'color': 4})
    doc.layers.new(name='TEXT', dxfattribs={'color': 7})
    
    # Draw T-Beam outline
    points = [
        (0, 0),
        (bf, 0),
        (bf, tf),
        ((bf + bw)/2, tf),
        ((bf + bw)/2, D),
        ((bf - bw)/2, D),
        ((bf - bw)/2, tf),
        (0, tf),
        (0, 0)
    ]
    msp.add_lwpolyline(points, dxfattribs={'layer': 'OUTLINE'})
    
    # Draw centerline
    msp.add_line((bf/2, 0), (bf/2, D), dxfattribs={'layer': 'CENTER', 'linetype': 'DASHED'})
    
    # Draw reinforcement
    cover = 25  # mm
    
    # Main tension bars
    bar_radius = main_bars_dia / 2
    bar_spacing = (bw - 2*cover - main_bars_dia) / (num_bars - 1) if num_bars > 1 else 0
    
    for i in range(num_bars):
        x = (bf - bw)/2 + cover + bar_radius + (i * bar_spacing if num_bars > 1 else 0)
        y = cover + bar_radius
        msp.add_circle((x, y), bar_radius, dxfattribs={'layer': 'REINFORCEMENT'})
    
    # Stirrups
    stirrup_width = bw - 2*cover - stirrup_dia
    stirrup_height = D - 2*cover - stirrup_dia
    
    # Draw stirrups at critical sections (supports and midspan)
    for x_offset in [0, L*1000/4, L*1000/2]:  # Start, quarter, and mid-span
        x = (bf - bw)/2 + cover + stirrup_dia/2 + x_offset
        points = [
            (x, cover + stirrup_dia/2),
            (x + stirrup_width, cover + stirrup_dia/2),
            (x + stirrup_width, cover + stirrup_dia/2 + stirrup_height),
            (x, cover + stirrup_dia/2 + stirrup_height),
            (x, cover + stirrup_dia/2)
        ]
        msp.add_lwpolyline(points, dxfattribs={'layer': 'REINFORCEMENT'})
    
    # Add dimensions
    msp.add_aligned_dim(
        p1=(0, -50),
        p2=(bf, -50),
        distance=-100,
        dimstyle='EZDXF',
        override={
            'dimtxsty': 'Standard',
            'dimtxt': 2.5,
            'dimgap': 1.0,
            'dimscale': 1.0
        }
    )
    
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
        f"T-BEAM SECTION",
        f"Flange: {bf} x {tf} mm",
        f"Web: {bw} x {D-tf} mm",
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
        ).set_pos((bf/2, y_offset - i * 7), align='MIDDLE_CENTER')
    
    # Save to bytes and return
    dxf_bytes = BytesIO()
    doc.saveas(dxf_bytes)
    dxf_bytes.seek(0)
    return dxf_bytes
