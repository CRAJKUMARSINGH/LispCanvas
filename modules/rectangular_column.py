import streamlit as st
import ezdxf
from io import BytesIO

def page_rectangular_column():
    st.title("Rectangular Column Designer")
    
    with st.sidebar:
        st.header("Design Parameters")
        
        # Column Dimensions
        st.subheader("Column Dimensions")
        width = st.number_input("Width (mm)", min_value=150.0, value=300.0, step=10.0)
        depth = st.number_input("Depth (mm)", min_value=150.0, value=450.0, step=10.0)
        height = st.number_input("Height (mm)", min_value=1000.0, value=3000.0, step=100.0)
        
        # Material Properties
        st.subheader("Material Properties")
        concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40"])
        steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"])
        
        # Reinforcement Details - Longer Side
        st.subheader("Longer Side Reinforcement")
        long_bars_num = st.number_input("Number of Bars (Long Side)", min_value=2, value=4, step=1)
        long_bars_dia = st.number_input("Bar Diameter (mm) - Long Side", min_value=8.0, value=16.0, step=2.0)
        
        # Reinforcement Details - Shorter Side
        st.subheader("Shorter Side Reinforcement")
        short_bars_num = st.number_input("Number of Bars (Short Side)", min_value=2, value=3, step=1)
        short_bars_dia = st.number_input("Bar Diameter (mm) - Short Side", min_value=8.0, value=16.0, step=2.0)
        
        # Ties
        st.subheader("Ties")
        tie_dia = st.number_input("Ties Diameter (mm)", min_value=6.0, value=8.0, step=1.0)
        tie_spacing = st.number_input("Tie Spacing (mm)", min_value=100.0, value=150.0, step=10.0)
        
        # Loads
        st.subheader("Design Loads")
        axial_load = st.number_input("Axial Load (kN)", min_value=0.0, value=1000.0, step=50.0)
        moment_major = st.number_input("Major Axis Moment (kNm)", min_value=0.0, value=75.0, step=5.0)
        moment_minor = st.number_input("Minor Axis Moment (kNm)", min_value=0.0, value=50.0, step=5.0)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Design Summary")
        st.write(f"**Concrete Grade:** {concrete_grade}")
        st.write(f"**Steel Grade:** {steel_grade}")
        st.write(f"**Column Size:** {width} x {depth} mm")
        st.write(f"**Column Height:** {height} mm")
        st.write(f"**Long Side Bars:** {long_bars_num} - Ø{long_bars_dia} mm")
        st.write(f"**Short Side Bars:** {short_bars_num} - Ø{short_bars_dia} mm")
        st.write(f"**Ties:** Ø{tie_dia} mm @ {tie_spacing} mm c/c")
    
    with col2:
        st.subheader("Load Summary")
        st.write(f"**Axial Load:** {axial_load} kN")
        st.write(f"**Major Axis Moment:** {moment_major} kNm")
        st.write(f"**Minor Axis Moment:** {moment_minor} kNm")
    
    # Generate DXF button
    if st.button("Generate DXF"):
        # Create a simple DXF representation
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()
        
        # Add column rectangle
        msp.add_lwpolyline([(0, 0), (width, 0), (width, depth), (0, depth), (0, 0)])
        
        # Add reinforcement bars - longer side (top and bottom)
        cover = 40  # mm cover
        x_spacing = (width - 2 * cover) / (long_bars_num - 1)
        for i in range(long_bars_num):
            x = cover + i * x_spacing
            msp.add_circle(center=(x, cover), radius=long_bars_dia/2)
            msp.add_circle(center=(x, depth - cover), radius=long_bars_dia/2)
        
        # Add reinforcement bars - shorter side (sides)
        y_spacing = (depth - 2 * cover) / (short_bars_num - 1)
        for i in range(1, short_bars_num - 1):  # Skip corners as they're already drawn
            y = cover + i * y_spacing
            msp.add_circle(center=(cover, y), radius=short_bars_dia/2)
            msp.add_circle(center=(width - cover, y), radius=short_bars_dia/2)
        
        # Add ties
        tie_radius = (width - 2 * cover + 2 * tie_dia/2) / 2
        tie_height = (depth - 2 * cover + 2 * tie_dia/2) / 2
        msp.add_lwpolyline([
            (cover - tie_dia/2, cover - tie_dia/2),
            (width - cover + tie_dia/2, cover - tie_dia/2),
            (width - cover + tie_dia/2, depth - cover + tie_dia/2),
            (cover - tie_dia/2, depth - cover + tie_dia/2),
            (cover - tie_dia/2, cover - tie_dia/2)
        ])
        
        # Save DXF to bytes
        dxf_bytes = BytesIO()
        doc.saveas(dxf_bytes)
        dxf_bytes.seek(0)
        
        # Download button
        st.download_button(
            label="Download DXF",
            data=dxf_bytes,
            file_name="rectangular_column.dxf",
            mime="application/dxf"
        )
