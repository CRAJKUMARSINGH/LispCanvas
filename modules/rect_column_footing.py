import streamlit as st
import ezdxf
from io import BytesIO

def page_rect_column_footing():
    st.title("Rectangular Column with Footing Designer")
    
    with st.sidebar:
        st.header("Column Parameters")
        
        # Column Dimensions
        st.subheader("Column Dimensions")
        col_width = st.number_input("Column Width (mm)", min_value=200.0, value=400.0, step=50.0)
        col_depth = st.number_input("Column Depth (mm)", min_value=200.0, value=600.0, step=50.0)
        col_height = st.number_input("Column Height (mm)", min_value=2000.0, value=3500.0, step=100.0)
        
        # Material Properties
        st.subheader("Material Properties")
        concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40"])
        steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"])
        
        # Column Reinforcement
        st.subheader("Column Reinforcement")
        # Longer Side
        long_bars_num = st.number_input("Number of Bars (Long Side)", min_value=2, value=5, step=1)
        long_bars_dia = st.number_input("Bar Diameter (mm) - Long Side", min_value=12.0, value=20.0, step=2.0)
        # Shorter Side
        short_bars_num = st.number_input("Number of Bars (Short Side)", min_value=2, value=3, step=1)
        short_bars_dia = st.number_input("Bar Diameter (mm) - Short Side", min_value=12.0, value=16.0, step=2.0)
        # Ties
        tie_dia = st.number_input("Ties Diameter (mm)", min_value=6.0, value=8.0, step=1.0)
        tie_spacing = st.number_input("Tie Spacing (mm)", min_value=100.0, value=150.0, step=10.0)
        
        # Footing Parameters
        st.header("Footing Parameters")
        footing_length = st.number_input("Footing Length (mm)", min_value=1000.0, value=2000.0, step=100.0)
        footing_width = st.number_input("Footing Width (mm)", min_value=1000.0, value=2500.0, step=100.0)
        footing_depth = st.number_input("Footing Depth (mm)", min_value=300.0, value=500.0, step=50.0)
        
        # Footing Reinforcement
        st.subheader("Footing Reinforcement")
        # Main Bars (along length)
        main_bars_dia = st.number_input("Main Bars Diameter (mm)", min_value=10.0, value=16.0, step=2.0)
        main_bars_spacing = st.number_input("Main Bars Spacing (mm)", min_value=100.0, value=150.0, step=10.0)
        # Distribution Bars (along width)
        dist_bars_dia = st.number_input("Distribution Bars Diameter (mm)", min_value=10.0, value=12.0, step=2.0)
        dist_bars_spacing = st.number_input("Distribution Bars Spacing (mm)", min_value=100.0, value=200.0, step=10.0)
        
        # Loads
        st.header("Design Loads")
        axial_load = st.number_input("Axial Load (kN)", min_value=100.0, value=2000.0, step=50.0)
        moment_major = st.number_input("Major Axis Moment (kNm)", min_value=0.0, value=150.0, step=10.0)
        moment_minor = st.number_input("Minor Axis Moment (kNm)", min_value=0.0, value=100.0, step=10.0)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Column Design")
        st.write(f"**Column Size:** {col_width} x {col_depth} mm")
        st.write(f"**Column Height:** {col_height} mm")
        st.write(f"**Long Side Bars:** {long_bars_num} - Ø{long_bars_dia} mm")
        st.write(f"**Short Side Bars:** {short_bars_num} - Ø{short_bars_dia} mm")
        st.write(f"**Ties:** Ø{tie_dia} mm @ {tie_spacing} mm c/c")
        
        st.subheader("Material Properties")
        st.write(f"**Concrete Grade:** {concrete_grade}")
        st.write(f"**Steel Grade:** {steel_grade}")
    
    with col2:
        st.subheader("Footing Design")
        st.write(f"**Footing Size:** {footing_length} x {footing_width} x {footing_depth} mm")
        st.write(f"**Main Bars:** Ø{main_bars_dia} mm @ {main_bars_spacing} mm c/c")
        st.write(f"**Distribution Bars:** Ø{dist_bars_dia} mm @ {dist_bars_spacing} mm c/c")
        
        st.subheader("Load Summary")
        st.write(f"**Axial Load:** {axial_load} kN")
        st.write(f"**Major Axis Moment:** {moment_major} kNm")
        st.write(f"**Minor Axis Moment:** {moment_minor} kNm")
    
    # Generate DXF button
    if st.button("Generate DXF"):
        # Create a simple DXF representation
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()
        
        # Add footing rectangle
        msp.add_lwpolyline([
            (0, 0), 
            (footing_length, 0), 
            (footing_length, footing_width), 
            (0, footing_width), 
            (0, 0)
        ])
        
        # Add column rectangle (centered on footing)
        col_x = (footing_length - col_width) / 2
        col_y = (footing_width - col_depth) / 2
        msp.add_lwpolyline([
            (col_x, col_y),
            (col_x + col_width, col_y),
            (col_x + col_width, col_y + col_depth),
            (col_x, col_y + col_depth),
            (col_x, col_y)
        ])
        
        # Add column reinforcement
        cover = 40  # mm cover
        
        # Main bars along length (top and bottom)
        x_spacing = (col_width - 2 * cover) / (long_bars_num - 1)
        for i in range(long_bars_num):
            x = col_x + cover + i * x_spacing
            # Top bars
            msp.add_circle(center=(x, col_y + cover), radius=long_bars_dia/2)
            # Bottom bars
            msp.add_circle(center=(x, col_y + col_depth - cover), radius=long_bars_dia/2)
        
        # Main bars along depth (sides)
        y_spacing = (col_depth - 2 * cover) / (short_bars_num - 1)
        for i in range(1, short_bars_num - 1):  # Skip corners as they're already drawn
            y = col_y + cover + i * y_spacing
            # Left bars
            msp.add_circle(center=(col_x + cover, y), radius=short_bars_dia/2)
            # Right bars
            msp.add_circle(center=(col_x + col_width - cover, y), radius=short_bars_dia/2)
        
        # Add footing reinforcement (top and bottom)
        # Main bars (along length)
        num_main_bars = int(footing_width / main_bars_spacing) + 1
        for i in range(num_main_bars):
            y = i * main_bars_spacing
            if y <= footing_width:
                msp.add_line((0, y), (footing_length, y))
        
        # Distribution bars (along width)
        num_dist_bars = int(footing_length / dist_bars_spacing) + 1
        for i in range(num_dist_bars):
            x = i * dist_bars_spacing
            if x <= footing_length:
                msp.add_line((x, 0), (x, footing_width))
        
        # Add ties around column
        msp.add_lwpolyline([
            (col_x + cover - tie_dia/2, col_y + cover - tie_dia/2),
            (col_x + col_width - cover + tie_dia/2, col_y + cover - tie_dia/2),
            (col_x + col_width - cover + tie_dia/2, col_y + col_depth - cover + tie_dia/2),
            (col_x + cover - tie_dia/2, col_y + col_depth - cover + tie_dia/2),
            (col_x + cover - tie_dia/2, col_y + cover - tie_dia/2)
        ])
        
        # Save DXF to bytes - Fixed the issue here using the correct approach
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as fp:
            temp_filename = fp.name
        doc.saveas(temp_filename)
        with open(temp_filename, 'rb') as f:
            dxf_content = f.read()
        os.unlink(temp_filename)
        
        # Download button
        st.download_button(
            label="Download DXF",
            data=dxf_content,
            file_name="rectangular_column_with_footing.dxf",
            mime="application/dxf"
        )