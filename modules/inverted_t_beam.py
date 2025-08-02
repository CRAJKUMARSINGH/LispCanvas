import streamlit as st
import ezdxf
import math
from io import BytesIO

def page_inverted_t_beam():
    st.title("Inverted T-Beam Designer")
    
    with st.sidebar:
        st.header("Beam Dimensions")
        
        # Flange Dimensions (now at bottom)
        st.subheader("Flange (Bottom) Dimensions")
        bf = st.number_input("Flange Width (mm)", min_value=500, value=1500, step=50)
        tf = st.number_input("Flange Thickness (mm)", min_value=50, value=150, step=10)
        
        # Web Dimensions
        st.subheader("Web Dimensions")
        bw = st.number_input("Web Width (mm)", min_value=100, value=300, step=10)
        d = st.number_input("Effective Depth (mm)", min_value=200, value=500, step=10)
        D = d + st.number_input("Clear Cover (mm)", min_value=15, value=30, step=5) + 10  # 10mm for half bar dia
        
        # Span
        st.subheader("Span & Support")
        L = st.number_input("Effective Span (m)", min_value=1.0, value=6.0, step=0.5)
        support_type = st.selectbox("Support Type", ["Simply Supported", "Continuous"])
        
        # Material Properties
        st.subheader("Material Properties")
        fck = st.number_input("fck (N/mm²)", min_value=15, value=25, step=5)
        fy = st.number_input("fy (N/mm²)", min_value=415, value=500, step=100, help="Characteristic strength of steel")
        
        # Loads
        st.subheader("Loads")
        dead_load = st.number_input("Dead Load (kN/m)", min_value=1.0, value=15.0, step=0.5)
        live_load = st.number_input("Live Load (kN/m)", min_value=1.0, value=20.0, step=0.5)
        
        # Reinforcement
        st.subheader("Reinforcement")
        main_bars_dia = st.number_input("Main Bars Diameter (mm)", min_value=10, value=20, step=2)
        num_bars = st.number_input("Number of Tension Bars", min_value=2, value=5, step=1)
        stirrup_dia = st.number_input("Stirrup Diameter (mm)", min_value=6, value=10, step=2)
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
        dxf_bytes = generate_inverted_t_beam_dxf(bf, tf, bw, D, d, main_bars_dia, num_bars, stirrup_dia, stirrup_spacing)
        
        # Download button
        st.download_button(
            label="Download Inverted T-Beam DXF",
            data=dxf_bytes,
            file_name=f"inverted_t_beam_{int(bf)}x{int(D)}.dxf",
            mime="application/dxf"
        )
        
        st.success("Inverted T-Beam DXF generated successfully!")
    
    # Design Calculations
    with st.expander("Design Calculations", expanded=False):
        st.subheader("Section Properties")
        area = (bf * tf) + ((D - tf) * bw)
        st.write(f"- Cross-sectional Area: {area / 1e6:.3f} m²")
        st.write(f"- Self Weight: {25 * area / 1e6:.2f} kN/m")
        
        st.subheader("Bending Design")
        # Simplified design calculations
        xu_lim = 0.48 * d  # For Fe415 and M20 concrete
        st.write(f"- Limiting Neutral Axis Depth: {xu_lim:.1f} mm")
        
        # Simplified moment capacity calculation
        mulim = 0.138 * fck * bw * d * d / 1e6  # kNm
        st.write(f"- Moment Capacity: {mulim:.2f} kNm")
        
        if max_moment > mulim:
            st.warning("Section is under-reinforced! Consider increasing dimensions or concrete grade.")
        else:
            st.success("Section is adequately reinforced.")
        
        st.subheader("Shear Design")
        # Simplified shear capacity calculation
        tau_c = 0.85 * math.sqrt(0.8 * fck) * (0.8 * fck / 6.89) ** 0.5  # N/mm²
        vuc = tau_c * bw * d / 1000  # kN
        st.write(f"- Concrete Shear Capacity: {vuc:.2f} kN")
        
        if max_shear > vuc:
            st.warning("Shear reinforcement required!")
            # Calculate required shear reinforcement
            vus = max_shear - vuc
            sv = (0.87 * fy * (2 * math.pi * (stirrup_dia/2)**2) * d) / (vus * 1000)  # mm
            st.write(f"- Required Stirrup Spacing: {sv:.0f} mm")
        else:
            st.success("Minimum shear reinforcement sufficient.")

def generate_inverted_t_beam_dxf(bf, tf, bw, D, d, main_bars_dia, num_bars, stirrup_dia, stirrup_spacing):
    """Generate DXF file for Inverted T-Beam section."""
    # Create a new DXF document
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()
    
    # Add layers
    doc.layers.new(name='OUTLINE', dxfattribs={'color': 7})  # White
    doc.layers.new(name='DIMENSIONS', dxfattribs={'color': 1})  # Red
    doc.layers.new(name='REINFORCEMENT', dxfattribs={'color': 1})  # Red
    doc.layers.new(name='TEXT', dxfattribs={'color': 7})  # White
    
    # Scale factor for drawing
    scale = 0.1  # 1:10 scale
    
    # Draw outline (inverted T-shape)
    points = [
        (0, 0),  # Bottom left
        (bf, 0),  # Bottom right
        (bf, tf),  # Top right of flange
        ((bf + bw)/2, tf),  # Start of web right
        ((bf + bw)/2, D),  # Top right of web
        ((bf - bw)/2, D),  # Top left of web
        ((bf - bw)/2, tf),  # End of web left
        (0, tf),  # Top left of flange
        (0, 0)  # Back to start
    ]
    
    # Draw outline
    msp.add_lwpolyline(points, close=True, dxfattribs={'layer': 'OUTLINE'})
    
    # Draw reinforcement
    # Main bars in flange (tension)
    bar_area = math.pi * (main_bars_dia/2)**2
    total_area = num_bars * bar_area
    
    # Distribute bars in flange
    bar_spacing = (bf - 2*40) / (num_bars - 1)  # 40mm cover on each side
    for i in range(num_bars):
        x = 40 + i * bar_spacing
        y = tf - 30  # 30mm cover from bottom of flange
        msp.add_circle((x, y), main_bars_dia/2, dxfattribs={'layer': 'REINFORCEMENT'})
    
    # Draw stirrups
    web_height = D - tf
    num_stirrups = int(web_height / stirrup_spacing) + 1
    
    for i in range(num_stirrups):
        y = tf + i * stirrup_spacing
        if y + stirrup_dia/2 > D:
            y = D - stirrup_dia/2
        
        # Draw stirrup (simplified as rectangle)
        points = [
            ((bf - bw)/2 + stirrup_dia/2, y),
            ((bf + bw)/2 - stirrup_dia/2, y),
            ((bf + bw)/2 - stirrup_dia/2, y + stirrup_dia),
            ((bf - bw)/2 + stirrup_dia/2, y + stirrup_dia),
            ((bf - bw)/2 + stirrup_dia/2, y)
        ]
        msp.add_lwpolyline(points, close=False, dxfattribs={'layer': 'REINFORCEMENT'})
    
    # Add dimensions
    def add_dim(p1, p2, offset, text):
        msp.add_aligned_dim(
            p1=p1,
            p2=p2,
            distance=offset,
            dimstyle='EZDXF',
            dxfattribs={'layer': 'DIMENSIONS'}
        ).set_text(text)
    
    # Add dimensions
    add_dim((0, 0), (bf, 0), -50, f"{bf}")  # Flange width
    add_dim((0, 0), (0, D), -50, f"{D}")  # Total depth
    add_dim((0, tf), (bf, tf), -100, f"{tf}")  # Flange thickness
    add_dim(((bf - bw)/2, tf), ((bf + bw)/2, tf), 50, f"{bw}")  # Web width
    
    # Save to bytes
    output = BytesIO()
    doc.saveas(output)
    output.seek(0)
    
    return output.getvalue()
