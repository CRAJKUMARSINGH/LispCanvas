import streamlit as st
import numpy as np
import ezdxf
from io import BytesIO

def page_circular_column_footing():
    st.title("Circular Column with Footing Designer")
    
    with st.sidebar:
        st.header("Column Parameters")
        
        # Column Dimensions
        st.subheader("Column Dimensions")
        col_diameter = st.number_input("Column Diameter (mm)", min_value=200.0, value=400.0, step=50.0)
        col_height = st.number_input("Column Height (mm)", min_value=2000.0, value=3500.0, step=100.0)
        
        # Material Properties
        st.subheader("Material Properties")
        concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40"])
        steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"])
        
        # Column Reinforcement
        st.subheader("Column Reinforcement")
        main_bars_dia = st.number_input("Main Bars Diameter (mm)", min_value=12.0, value=20.0, step=2.0)
        num_bars = st.number_input("Number of Bars", min_value=6, value=8, step=1)
        tie_dia = st.number_input("Ties Diameter (mm)", min_value=6.0, value=8.0, step=1.0)
        tie_spacing = st.number_input("Tie Spacing (mm)", min_value=100.0, value=150.0, step=10.0)
        
        # Footing Parameters
        st.header("Footing Parameters")
        footing_dia = st.number_input("Footing Diameter (mm)", min_value=1000.0, value=2000.0, step=100.0)
        footing_depth = st.number_input("Footing Depth (mm)", min_value=300.0, value=500.0, step=50.0)
        
        # Footing Reinforcement
        st.subheader("Footing Reinforcement")
        footing_top_bars_dia = st.number_input("Top Bars Diameter (mm)", min_value=10.0, value=12.0, step=2.0)
        footing_top_spacing = st.number_input("Top Bars Spacing (mm)", min_value=100.0, value=150.0, step=10.0)
        footing_bottom_bars_dia = st.number_input("Bottom Bars Diameter (mm)", min_value=10.0, value=16.0, step=2.0)
        footing_bottom_spacing = st.number_input("Bottom Bars Spacing (mm)", min_value=100.0, value=150.0, step=10.0)
        
        # Loads
        st.header("Design Loads")
        axial_load = st.number_input("Axial Load (kN)", min_value=100.0, value=1500.0, step=50.0)
        moment_x = st.number_input("Moment about X (kNm)", min_value=0.0, value=100.0, step=10.0)
        moment_y = st.number_input("Moment about Y (kNm)", min_value=0.0, value=100.0, step=10.0)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Column Design")
        st.write(f"**Column Diameter:** {col_diameter} mm")
        st.write(f"**Column Height:** {col_height} mm")
        st.write(f"**Main Bars:** {num_bars} - Ø{main_bars_dia} mm")
        st.write(f"**Ties:** Ø{tie_dia} mm @ {tie_spacing} mm c/c")
        
        st.subheader("Footing Design")
        st.write(f"**Footing Diameter:** {footing_dia} mm")
        st.write(f"**Footing Depth:** {footing_depth} mm")
        st.write(f"**Top Reinforcement:** Ø{footing_top_bars_dia} mm @ {footing_top_spacing} mm c/c")
        st.write(f"**Bottom Reinforcement:** Ø{footing_bottom_bars_dia} mm @ {footing_bottom_spacing} mm c/c")
    
    with col2:
        st.subheader("Material Properties")
        st.write(f"**Concrete Grade:** {concrete_grade}")
        st.write(f"**Steel Grade:** {steel_grade}")
        
        st.subheader("Load Summary")
        st.write(f"**Axial Load:** {axial_load} kN")
        st.write(f"**Moment X:** {moment_x} kNm")
        st.write(f"**Moment Y:** {moment_y} kNm")
    
    # Generate DXF button
    if st.button("Generate DXF"):
        # Create a simple DXF representation
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()
        
        # Add footing circle
        msp.add_circle(center=(0, 0), radius=footing_dia/2)
        
        # Add column circle
        msp.add_circle(center=(0, 0), radius=col_diameter/2)
        
        # Add column reinforcement
        cover = 40  # mm cover
        for i in range(num_bars):
            angle = 2 * np.pi * i / num_bars
            x = (col_diameter/2 - cover) * np.cos(angle)
            y = (col_diameter/2 - cover) * np.sin(angle)
            msp.add_circle(center=(x, y), radius=main_bars_dia/2)
        
        # Add footing reinforcement (top and bottom)
        num_top_bars = int(np.ceil(np.pi * (footing_dia - 2*cover) / footing_top_spacing))
        num_bottom_bars = int(np.ceil(np.pi * (footing_dia - 2*cover) / footing_bottom_spacing))
        
        # Top reinforcement
        for i in range(num_top_bars):
            angle = 2 * np.pi * i / num_top_bars
            x = (footing_dia/2 - cover) * np.cos(angle)
            y = (footing_dia/2 - cover) * np.sin(angle)
            msp.add_circle(center=(x, y), radius=footing_top_bars_dia/2)
        
        # Bottom reinforcement (slightly larger radius)
        for i in range(num_bottom_bars):
            angle = 2 * np.pi * i / num_bottom_bars
            x = (footing_dia/2 - cover - 50) * np.cos(angle)
            y = (footing_dia/2 - cover - 50) * np.sin(angle)
            msp.add_circle(center=(x, y), radius=footing_bottom_bars_dia/2)
        
        # Save DXF to bytes
        dxf_bytes = BytesIO()
        doc.saveas(dxf_bytes)
        dxf_bytes.seek(0)
        
        # Download button
        st.download_button(
            label="Download DXF",
            data=dxf_bytes,
            file_name="circular_column_with_footing.dxf",
            mime="application/dxf"
        )

page_circular_column_footing()
