import streamlit as st
import numpy as np
import ezdxf
from io import BytesIO

def page_circular_column():
    st.title("Circular Column Designer")
    
    with st.sidebar:
        st.header("Design Parameters")
        
        # Column Dimensions
        st.subheader("Column Dimensions")
        diameter = st.number_input("Diameter (mm)", min_value=100.0, value=300.0, step=10.0)
        height = st.number_input("Height (mm)", min_value=1000.0, value=3000.0, step=100.0)
        
        # Material Properties
        st.subheader("Material Properties")
        concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40"])
        steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"])
        
        # Reinforcement Details
        st.subheader("Reinforcement")
        main_bars_dia = st.number_input("Main Bars Diameter (mm)", min_value=8.0, value=16.0, step=2.0)
        num_bars = st.number_input("Number of Bars", min_value=4, value=6, step=1)
        tie_dia = st.number_input("Ties Diameter (mm)", min_value=6.0, value=8.0, step=1.0)
        tie_spacing = st.number_input("Tie Spacing (mm)", min_value=100.0, value=150.0, step=10.0)
        
        # Loads
        st.subheader("Design Loads")
        axial_load = st.number_input("Axial Load (kN)", min_value=0.0, value=1000.0, step=50.0)
        moment_x = st.number_input("Moment about X (kNm)", min_value=0.0, value=50.0, step=5.0)
        moment_y = st.number_input("Moment about Y (kNm)", min_value=0.0, value=50.0, step=5.0)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Design Summary")
        st.write(f"**Concrete Grade:** {concrete_grade}")
        st.write(f"**Steel Grade:** {steel_grade}")
        st.write(f"**Column Diameter:** {diameter} mm")
        st.write(f"**Column Height:** {height} mm")
        st.write(f"**Main Bars:** {num_bars} - Ø{main_bars_dia} mm")
        st.write(f"**Ties:** Ø{tie_dia} mm @ {tie_spacing} mm c/c")
    
    with col2:
        st.subheader("Load Summary")
        st.write(f"**Axial Load:** {axial_load} kN")
        st.write(f"**Moment X:** {moment_x} kNm")
        st.write(f"**Moment Y:** {moment_y} kNm")
    
    # Generate DXF button
    if st.button("Generate DXF"):
        # Create a simple DXF representation
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()
        
        # Add column circle
        msp.add_circle(center=(0, 0), radius=diameter/2)
        
        # Add reinforcement bars
        for i in range(num_bars):
            angle = 2 * np.pi * i / num_bars
            x = (diameter/2 - 40) * np.cos(angle)
            y = (diameter/2 - 40) * np.sin(angle)
            msp.add_circle(center=(x, y), radius=main_bars_dia/2)
        
        # Add ties
        msp.add_circle(center=(0, 0), radius=diameter/2 - 30)
        
        # Save DXF to bytes
        dxf_bytes = BytesIO()
        doc.saveas(dxf_bytes)
        dxf_bytes.seek(0)
        
        # Download button
        st.download_button(
            label="Download DXF",
            data=dxf_bytes,
            file_name="circular_column.dxf",
            mime="application/dxf"
        )
